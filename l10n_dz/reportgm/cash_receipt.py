import time
from openerp.report import report_sxw

 

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
        
        
        
       
 
 
#report_sxw.report_sxw('report.sale.collection_docket', 'sale.order', 'addons/module/report/collection_docket.rml', parser=order, header="external")
report_sxw.report_sxw('report.sale.cash_receipt', 'account.voucher', 'addons/l10n_dz/reportgm/cash_receipt.rml', parser=order, header="external")