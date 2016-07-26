# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models

class ResCommune(models.Model):
    _name='res.commune'
    _description='commune'
    
    code = fields.Char('Code Commune', size=2, help='Le code de la commune sur deux positions.', required=True)
    state_id = fields.Many2one('res.country.state', 'Wilaya', required=True)
    name = fields.Char('Commune', required=True, help='Commune')
        
class FormJuridique(models.Model):
    _name='forme.juridique'
    _description='Forme juridique'

    code =  fields.Char('Code')
    name = fields.Char('Nom')
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True,
        default=lambda self: self.env['res.company']._company_default_get('forme.juridique'))

    _sql_constraints = [
        ('name_uniq', 'unique(company_id, name)',
            'Forme juridique must be unique per Company!'),
    ]

class ResCompany(models.Model):
    _inherit = 'res.company'

    nis = fields.Char("N° d'Identification Statistique")
    ai = fields.Char("Article d\'Imposition")
    frmjuri = fields.Many2one("forme.juridique","Forme juridique")
    commune_id = fields.Many2one("res.commune", "Commune")
    
    nif = fields.Char("N° d'Identification fiscal")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rc  = fields.Char("N° Registre de Commerce")
    nif = fields.Char("N° d'Identification Fiscale")
    nis = fields.Char("N° d'identification Statistique")
    ai  = fields.Char("Article d'Imposition")
    frmjuri = fields.Many2one("forme.juridique","Forme juridique")
    commune_id = fields.Many2one("res.commune", "Commune")

    _sql_constraints = [
        ('rc_uniq', 'unique(company_id, rc)',
            'RC must be unique per Company!'),
    ]    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
