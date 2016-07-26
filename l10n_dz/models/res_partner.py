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
from openerp import models, fields, api, exceptions, _
import re
from openerp.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #ajout de champs
    rc = fields.Char("N° RC", size=15)
    nis = fields.Char("N.I.S", size=15)
    ai = fields.Char("A.I", size=11)
    # company_registry = fields.Char(string="N° R.C", required=True, size=15)
    nif = fields.Char("N.I.F", size=15)
    frmjuri = fields.Many2one('forme.juridique','Forme juridique',)
    commune_id = fields.Many2one("res.country.state.commune", 'Commune')

    # def _get_default_payment(self, cr, uid, context=None):
    #     res = self.pool.get('account.payment.term').search(cr, uid, [('name','=','Immediate Payment')], context=context)
    #     print "======== %s" %(res)
    #     return res and res[0] or False

    # property_payment_term = fields.Many2one("account.payment.term", string ="Customer Payment Term", help="This payment term will be used instead of the default one for sale order and customer invoice", default=_get_default_payment)


    @api.constrains('rc')
    def is_valid_rc(self):
        pattern ="^[a-zA-Z0-9]{15}$"
        for data in self:
            if data.rc:
                if not re.match(pattern, data.rc):
                    raise ValidationError("Veuillez verifier le R.C")

    @api.constrains('nif')
    def is_valid_nif(self):
        pattern ="^[a-zA-Z0-9]{15}$"
        for data in self:
            if data.nif:
                if not re.match(pattern, data.nif):
                    raise ValidationError("Veuillez verifier le N.I.F")

    @api.constrains('nis')
    def is_valid_nis(self):
        pattern ="^[a-zA-Z0-9]{15}$"
        for data in self:
            if data.nis:
                if not re.match(pattern, data.nis):
                    raise ValidationError("Veuillez verifier le N.I.S")

    @api.constrains('ai')
    def is_valid_ai(self):
        pattern ="^[a-zA-Z0-9]{11}$"
        for data in self:
            if data.ai:
                if not re.match(pattern, data.ai):
                    raise ValidationError("Veuillez verifier le A.I")

    def onchange_state(self, cr, uid, ids, wilaya_id, context=None):
        val = {}
        company_val=super(ResPartner,self).onchange_state(cr, uid,ids, wilaya_id, context=context)
        commune_ids = self.pool.get('res.country.state.commune').search(cr, uid, [('state_id', '=', wilaya_id)], context=context)
        val['domain'] = {'commune_id':[('id', 'in', commune_ids)]}
        val['value'] = company_val
        return val
