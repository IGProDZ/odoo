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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
import convertion
import re

#ajout du champ domiciliation bancaire
class account_invoice(models.Model):
# ajout du champ domiciliation bancaire au niveau de la vue facture
    _inherit = 'account.invoice'

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount', 'payment_term')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)
        self.amount_total = self.amount_untaxed + self.amount_tax
        self.amount_timbre = self._timbre(self.amount_total)
        self.total_timbre = self.amount_total + self.amount_timbre
        self.text_amount = self._text_amounts(self.amount_total)

    @api.multi
    def _timbre(self, amount_total):
        timbre = 0
        # cash = self.payment_term and self.payment_term.payment_type or False
        # if cash == 'cash':
        timbre = self.env['config.timbre']._timbre(amount_total)
        return timbre

    @api.multi
    def onchange_payment_term(self, payment):
        val ={}
        if not payment:
            return {'value': {'type_payment': False}}
        part =  self.env['account.payment.term'].browse(payment)
        payment_type =  part.payment_type or False
        val = {'payment_type': payment_type}
        return {'value': val}

    @api.multi
    def _text_amounts(self, amount):
        total_timbre = convertion.trad(amount,'dinar').upper()
        return total_timbre

    dmb=fields.Char('Domiciliation bancaire', size=20)
    payment_type = fields.Char('')
    amount_timbre = fields.Float(string='Timbre', digits=dp.get_precision('Account'),
     readonly=True, compute='_compute_amount', track_visibility='always')
    total_timbre = fields.Float(string='Total', digits=dp.get_precision('Account'), store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    text_amount = fields.Text(string='', store=True, readonly=True, compute='_compute_amount', track_visibility='always')
