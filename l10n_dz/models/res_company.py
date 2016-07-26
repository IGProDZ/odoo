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
import openerp.addons.decimal_precision as dp

class ResCompany(models.Model):
    _inherit = 'res.company'

    #ajout de champs
    nis = fields.Char("N.I.S", size=15)
    ai = fields.Char("A.I", required=True, size=11)
    company_registry = fields.Char(string="N° R.C", required=True, size=15)
    nif = fields.Char("N.I.F", size=15)
    frmjuri = fields.Many2one('forme.juridique','Forme juridique',)
    commune_id = fields.Many2one("res.country.state.commune", 'Commune')
    capital_social = fields.Float("Capital Social", digits=dp.get_precision('Account'), required=True, help="Society Social Capital")

    @api.constrains('company_registry')
    def is_valid_rc(self):
        pattern ="^[a-zA-Z0-9]{15}$"
        for data in self:
            if data.company_registry:
                if not re.match(pattern, data.company_registry):
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
