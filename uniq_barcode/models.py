# -*- coding: utf-8 -*-
from openerp import models, api, _
from openerp.exceptions import Warning


class uni_barcode(models.Model):
    _inherit = "product.product"


    @api.one
    @api.constrains('company_id', 'ean13', 'active')
    def check_unique_company_and_ean13(self):
        if self.active and self.ean13 and self.company_id:
            filters = [('company_id', '=', self.company_id.id),
                       ('ean13', '=', self.ean13), ('active', '=', True)]
            prod_ids = self.search(filters)
            if len(prod_ids) > 1:
                raise Warning(
                    _('Ce code-barres existe deja!'))
