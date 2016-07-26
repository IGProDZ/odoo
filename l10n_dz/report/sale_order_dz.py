# -*- coding: utf-8 -*-
#!/usr/bin/env pythons
from sale.report import sale_order
from integerToWords_fr import final_result

from openerp.report import report_sxw
from netsvc import Service
del Service._services['report.sale.order'] 


# create a custom parser inherited from sale order parser:
class new_order_report(sale_order.order):
    '''Custom parser with an additional method
    '''
    def __init__(self, cr, uid, name, context):
        super(new_order_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'final_result':final_result,
            'display_lettre': self.display_lettre,  #affichage :arrêtée la présente facture à la somme de: traite les accents
        }) 
        
        
    def display_lettre(self):
         x= 'arrêtée la  présente facture à la somme de :'
         return x
    
    
    
# remove previous sale.report service :


# register the new report service :
report_sxw.report_sxw('report.sale.order','sale.order','addons/l10n_dz/report/sale_order_dz.rml',parser=new_order_report)


