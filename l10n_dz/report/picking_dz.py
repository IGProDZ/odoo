from stock.report import picking
from openerp.report import report_sxw
from integerToWords_fr import final_result

class picking_new(picking.picking):
    def __init__(self, cr, uid, name, context):
        super(picking_new, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'final_result':final_result,
        })
    """def get_product_desc(self, move_line):
        desc = move_line.product_id.name
        if move_line.product_id.default_code:
            desc = '[' + move_line.product_id.default_code + ']' + ' ' + desc
        return desc"""

from netsvc import Service
for serv in ['', '.in', '.out']: del Service._services['report.stock.picking.list' + serv]

for suffix in ['', '.in', '.out']:
    report_sxw.report_sxw('report.stock.picking.list' + suffix,
                          'stock.picking' + suffix,
                          'addons/l10n_dz/report/picking_dz.rml',
                          parser=picking_new)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
