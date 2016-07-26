# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Kheireddine Yacine BENSIDHOUM le_dilem@yahoo.fr
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from common import AdditionalDiscountable
from openerp.tools.translate import _
import convertion
from math import ceil


class config_timbre(osv.Model):
    _name='config.timbre'
    _description='Timbre Fiscal'

    def _timbre_voucher(self, cr, uid, montant):
        add_timbre_amt = 0.0
        obj = self.pool.get('config.timbre')
        ids_obj = obj.search(cr, uid, [])
        if not ids_obj :
            return False
        dict = obj.read(cr, uid, ids_obj[0])
        if dict['min_value_stop'] >= montant >= dict['min_value_go']:
            add_timbre_amt = dict['min_value']
        elif montant > dict['min_value_stop'] :
            add_timbre = (montant * dict['prix']) / dict['tranche']
            add_timbre_amt = ceil(add_timbre)
            if add_timbre_amt >= dict['max_value']:
                add_timbre_amt = dict['max_value']
        return add_timbre_amt + montant

    def _timbre(self, cr, uid, montant):
        add_timbre_amt = 0.0
        obj = self.pool.get('config.timbre')
        ids_obj = obj.search(cr, uid, [])
        if not ids_obj :
            return False
        dict = obj.read(cr, uid, ids_obj[0])
        if dict['min_value_stop'] >= montant >= dict['min_value_go']:
            add_timbre_amt = dict['min_value']
        elif montant > dict['min_value_stop'] :
            add_timbre = (montant * dict['prix']) / dict['tranche']
            add_timbre_amt = ceil(add_timbre)
            if add_timbre_amt >= dict['max_value']:
                add_timbre_amt = dict['max_value']
        return add_timbre_amt
    _columns = {
        'name': fields.char('Name'),
        'tranche': fields.float('Tranche', digits_compute=dp.get_precision('Product Price'),required=True),
        'prix': fields.float('Prix', digits_compute=dp.get_precision('Product Price'),required=True),
        'min_value_go': fields.float('Valeur Minimale', digits_compute=dp.get_precision('Product Price'),required=True),
        'min_value_stop': fields.float('Valeur Maximale', digits_compute=dp.get_precision('Product Price'),required=True),
        'min_value': fields.float('Montant dû', digits_compute=dp.get_precision('Product Price'),required=True),
        'max_value': fields.float('Plafond', digits_compute=dp.get_precision('Product Price'),required=True),
        'sale_timbre': fields.many2one('account.account','Compte Contrepartie Vente'),
        'purchase_timbre': fields.many2one('account.account','Compte Contrepartie Achat'),
    }

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'name must be unique per Company!'),
    ]

class sale_order(AdditionalDiscountable,osv.Model):

    _inherit = 'sale.order'

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    def _amount_all(self, *args, **kwargs):
        return self._amount_all_generic(sale_order, *args, **kwargs)

    def _text_amount(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for amount in self.browse(cr, uid, ids, context=context):
            result[amount.id] = convertion.trad(amount.amount_total,'dinar').upper()

        return result

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        val = {}
        partner_val = super(sale_order, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        # for partner  in self.browse(cr, uid, ids):
        if not partner_val['value']['payment_term']:
            payment_id = self.pool.get('account.payment.term').search(cr, uid, [('name', '=', 'Paiement immédiat')], context=context)
            payment = self.pool.get('account.payment.term').browse(cr, uid, payment_id)
            partner_val['value']['payment_term'] = payment.id

        val = partner_val['value']
        print val
        return {'value': val}


    #payment term
    def onchange_payment_term(self, cr, uid, ids, payment, context=None):
        if not payment:
            return {'value': {'type_payment': False}}
        part = self.pool.get('account.payment.term').browse(cr, uid, payment, context=context)
        payment_type = part.payment_type or False
        val = {'payment_type': payment_type}
        return {'value': val}

    _columns = {

        'payment_type': fields.char('Payment Type', size=128),
        'amount_timbre': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Timbre', multi='sums', help="Timbre."),

        'total_timbre': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total', multi='sums', help="The total amount."),

        'text_amount': fields.function(_text_amount, method=True, string=_("Text amount"), type="char"),
    }


    def _get_default_payment(self, cr, uid, context=None):

        res = self.pool.get('account.payment.term').search(cr, uid, [('name','=','Immediate Payment')], context=context)
        print "=========================================== %s" %(res)
        return res and res[0] or False

    defaults = {'payment_type':'immediat',
                'payment_term':_get_default_payment,
    }

    def _make_invoice(self, cr, uid, order, lines, context=None):
        """Add a Timbre in the invoice after creation, and recompute the total
        """
        inv_obj = self.pool.get('account.invoice')
        # create the invoice
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context)
        # modify the invoice
        inv_obj.write(cr, uid, [inv_id], {'total_timbre': order.total_timbre or 0.0 ,
                                          'payment_type' :order.payment_type or False},
                      context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id
