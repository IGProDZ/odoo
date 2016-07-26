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

class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    commune_ids = fields.One2many('res.country.state.commune', 'state_id', 'Communes')


class ResCountryCtateCommune(models.Model):
    _name='res.country.state.commune'
    code= fields.Char('Code Commune', size=2, help='Le code de la commune sur deux positions.', required=True)
    state_id= fields.Many2one('res.country.state', 'Wilaya', required=True)
    name=fields.Char('Commune', size=64, required=True, help='Commune')