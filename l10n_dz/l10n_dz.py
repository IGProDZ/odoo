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

from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
from logging import Logger
logger = logging.getLogger('trainings module')
 
#commentaire test
#test

class l10n_fr_report(osv.osv):
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
    
   #ajout de champs 

    _columns = {
        'nis': fields.char("N° d'Identification Statistique", size=30),
        'ai': fields.char("Article d'Imposition", size=30),
        'frmjuri': fields.many2one('forme.juridique','Forme juridique',),
        'commune_id': fields.many2one("res.commune", 'Commune'),
        
        'nif': fields.char("N° d'Identification fidcal", size=30),
    }
    
    
    
    #modifie le pied de page
    def onchange_footerdz(self, cr, uid, ids, custom_footer, phone, fax,ai,nis, email, website, vat, company_registry, bank_ids, context=None):
        if custom_footer:
            return {}

        # first line (notice that missing elements are filtered out before the join)
        res = ' | '.join(filter(bool, [
            phone            and '%s: %s' % (_('Phone'), phone),
            fax              and '%s: %s' % (_('Fax'), fax),
            email            and '%s: %s' % (_('Email'), email),
            website          and '%s: %s' % (_('Website'), website),
            vat              and '%s: %s' % (_('NIF'), vat),
            company_registry and '%s: %s' % (_('RC'), company_registry),
            ai               and '%s: %s' % (_('AI'),ai),
            nis               and '%s: %s' % (_('NIS'),nis),
            
        ]))
        # second line: bank accounts
        res_partner_bank = self.pool.get('res.partner.bank')
        account_data = self.resolve_2many_commands(cr, uid, 'bank_ids', bank_ids, context=context)
        account_names = res_partner_bank._prepare_name_get(cr, uid, account_data, context=context)
        if account_names:
            title = _('Bank Accounts') if len(account_names) > 1 else _('Bank Account')
            res += '\n%s: %s' % (title, ', '.join(name for id, name in account_names))

        return {'value': {'rml_footer': res, 'rml_footer_readonly': res}}

res_company()


class res_partner(osv.osv):
    _inherit = 'res.partner'
    

    _columns = {
        'rc': fields.char("N° Registre de Commerce", size=30),
        'nif': fields.char("N° d'Identification Fiscale", size=30),
        'nis': fields.char("N° d'identification Statistique", size=30),
        'ai': fields.char("Article d'Imposition", size=30),
        'frmjuri': fields.many2one('forme.juridique','Forme juridique'),
        'commune_id': fields.many2one("res.commune", 'Commune'), 
        
        
       
         
    }

res_partner()

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

account_journal()

#ajout du champ domiciliation bancaire
class account_invoice(osv.osv):
# ajout du champ domiciliation bancaire au niveau de la vue facture
    _inherit = 'account.invoice'
    _columns = {
        'dmb': fields.char('Domiciliation bancaire', size=20),}
account_invoice()

class res_commune(osv.osv):
    _name='res.commune'
    
    _columns = {
        'code': fields.char('Code Commune', size=2, help='Le code de la commune sur deux positions.', required=True),
        'state_id': fields.many2one('res.country.state', 'Wilaya', required=True),            
        'name': fields.char('Commune', size=64, required=True, help='Commune'),        
        }
    
res_commune()


    