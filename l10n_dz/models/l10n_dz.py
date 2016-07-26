# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import openerp
from openerp import SUPERUSER_ID, tools
from openerp.exceptions import ValidationError
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import convertion
import logging
import re
from logging import Logger
logger = logging.getLogger('trainings module')

#commentaire test
#test

class l10n_fr_report(osv.Model):
    _name = 'l10n.fr.report'
    _description = 'Report for l10n_fr'
    _columns = {
        'code': fields.char('Code', size=64),
        'name': fields.char('Name', size=128),
        'line_ids': fields.one2many('l10n.fr.line', 'report_id', 'Lines'),
    }
    _sql_constraints = [
        ('code_uniq', 'unique (code)','The code report must be unique !')
    ]

l10n_fr_report()

class l10n_fr_line(osv.osv):
    _name = 'l10n.fr.line'
    _description = 'Report Lines for l10n_fr'
    _columns = {
        'code': fields.char('Variable Name', size=64),
        'definition': fields.char('Definition', size=512),
        'name': fields.char('Name', size=256),
        'report_id': fields.many2one('l10n.fr.report', 'Report'),
    }
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The variable name must be unique !')
    ]

l10n_fr_line()


class res_company(osv.osv):
    _inherit = 'res.company'

    #modifie.7 le pied de page
    def onchange_footerdz(self, cr, uid, ids, custom_footer, phone, fax,ai,nis, email, website, nif, company_registry, capital_social, bank_ids, context=None):
        # if custom_footer:
        #     return {}
        # first line (notice that missing elements are filtered out before the join)
        res = ' | '.join(filter(bool, [
            phone            and '%s: %s' % (_('Phone'),phone),
            fax              and '%s: %s' % (_('Fax'),fax),
            email            and '%s: %s' % (_('Email'),email),
            website          and '%s: %s' % (_('Website'),website),
            nif              and '%s: %s' % (_('NIF'),nif),
            company_registry and '%s: %s' % (_('RC'),company_registry),
            ai               and '%s: %s' % (_('AI'),ai),
            nis              and '%s: %s' % (_('NIS'),nis),
            capital_social   and '%s: %s' % (_('Capital Social'),capital_social),
        ]))

        # second line: bank accounts
        res_partner_bank = self.pool.get('res.partner.bank')
        account_data = self.resolve_2many_commands(cr, uid, 'bank_ids', bank_ids, context=context)
        account_names = res_partner_bank._prepare_name_get(cr, uid, account_data, context=context)
        if account_names:
            title = _('Bank Accounts') if len(account_names) > 1 else _('Bank Account')
            res += '\n%s: %s' % (title, ', '.join(name for id, name in account_names))
        return {'value': {'rml_footer': res, 'rml_footer_readonly': res, 'custom_footer': True}}

res_company()

class form_juridique(osv.osv):
    _name='forme.juridique'

    _columns = {
        'code': fields.char('Code', size=30),
        'name': fields.char('Nom', size=60),
        }

 # Concaténation du Code et du Nom  dans les vues Partner et Company
    def name_get(self, cr, uid, ids, context=None):
        result = []
        for frmjuri in self.browse(cr, uid, ids, context):
            result.append((frmjuri.id, (frmjuri.code and (frmjuri.code + ' - ') or '') + frmjuri.name))
        return result


form_juridique()

class res_currency(osv.osv):
    _inherit = 'res.currency'
    _defaults ={
                'active': 0,

               }

res_currency()

class account_journal(osv.osv):

    _inherit = 'account.journal'

    def _default_cashbox_line_ids(self, cr, uid, context=None):
        # Return a list of coins in Dinar.
        result = [
            dict(pieces=value) for value in [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
        ]
        return result
    _defaults = {
        'cashbox_line_ids' : _default_cashbox_line_ids,
    }

    _columns = {
        'timbre_id':fields.many2one('account.tax','Timbre'),
    }


account_journal()

class account_voucher(osv.Model):
    _inherit = 'account.voucher'

    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=None):
        if context is None:
            context = {}
        if not journal_id:
            return False
        journal_pool = self.pool.get('account.journal')
        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        account_id = journal.default_credit_account_id or journal.default_debit_account_id
        tax_id = False
        if account_id and account_id.tax_ids:
            tax_id = account_id.tax_ids[0].id
        vals = {'value':{} }
        if ttype in ('sale', 'purchase'):
            vals = self.onchange_price(cr, uid, ids, line_ids, tax_id, partner_id, context)
            vals['value'].update({'tax_id':tax_id,'amount': amount,})
        currency_id = False
        print "===================================="
        print journal.currency
        if journal.currency:
            currency_id = journal.currency.id
        else:
            currency_id = journal.company_id.currency_id.id
        vals['value'].update({'currency_id': currency_id})
        #in case we want to register the payment directly from an invoice, it's confusing to allow to switch the journal
        #without seeing that the amount is expressed in the journal currency, and not in the invoice currency. So to avoid
        #this common mistake, we simply reset the amount to 0 if the currency is not the invoice currency.
        if context.get('payment_expected_currency') and currency_id != context.get('payment_expected_currency'):
            vals['value']['amount'] = 0
            amount = 0
        if journal.type != 'cash':
            if context.get('default_amount'):
                old_amount = context.get('default_amount')

            else:
                old_amount = 0
            vals['value'].update({'amount': old_amount})
        else:
            timbre =  self.pool.get('config.timbre')._timbre(cr, uid, amount)
            new_amount =  amount + timbre
            timbre_id = self.pool.get('config.timbre').search(cr, uid, [], context=context)
            timbre = self.pool.get('config.timbre').browse(cr,uid, timbre_id, context=context)
            acc= False
            if ttype not in ['sale']:
                acc= timbre.sale_timbre
            else:
                acc=timbre.purchase_timbre
            vals['value'].update({'amount': new_amount,
                                  'payment_option':'with_writeoff',
                                  'writeoff_acc_id': acc ,
                                  'comment':'Timbre'})
        if partner_id:
            res = self.onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context)
            for key in res.keys():
                vals[key].update(res[key])
        return vals


class account_payment_term(osv.osv):

    _inherit = 'account.payment.term'
    _columns = {
        'taxes_id': fields.many2many('account.tax', 'produ_taxes_rel',
                                     'prod_id', 'tax_id', 'Customer Taxes', domain=[('parent_id','=',False),('type_tax_use','in',['sale','all'])]),
        'payment_type': fields.selection([('immediat','Immédiat'),('terme','A terme'),],'Type', required=True),
    }
