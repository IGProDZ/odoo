# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class Ean13(models.Model):
    _inherit = 'product.product'

    ean13 = fields.Char(string ="Code-barres", size=50, help="Code-barres sans contrainte")
    default_code = fields.Char(string ="Code article")

    def _check_ean_key(self, cr, uid, ids, context=None):
        return True

    _constraints = [(_check_ean_key, 'override function', ['ean13'])]

