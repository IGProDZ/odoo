# -*- coding: utf-8 -*-
# (c) 2016 - IgPro
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Algeria - Accounting',
    'version': '1.0 alpha',
    'author': 'IGPro',
    'website': 'www.igpro-online.net',
    'category': 'Localization/Account Charts',
    "contributors": [
        "1 <Sid Ahmed MOKEDDEM",
    ],
    'description': """
This is the module to manage the accounting chart for Algeria in odoo.
========================================================================


""",
    'depends': [
        'account', 'account_chart',
        'procurement', 'board',
        'sale',
        'purchase',
        'stock',
	'account_accountant',
        'account_voucher',
    ],
    'data': [
        'data/dz_plan_comptable_normalise.xml',
        'data/l10n_dz_wizard.xml',
        'data/dz_pcg_taxes.xml',
        'data/dz_tax.xml',
        'data/dz_fiscal_templates.xml',
        'data/dz_form_juridique.xml',
        'data/dz_bank.xml',
        'data/dz_wilayas.xml',
        'data/commune.xml',
        'security/ir.model.access.csv',
        'report/stock_report_dz.xml',
        'wizard/dz_report_bilan_view.xml',
        'wizard/dz_report_compute_resultant_view.xml',
        'wizard/dz_report_tft_view.xml',
        'view/l10n_dz_view.xml',
        'data/dz_report.xml',
        'reportgm/reports.xml',
        'view/timbre_view.xml',
        'view/payment_term_view.xml',
        'view/sale_view.xml',
        'view/account_invoice_view.xml',
        'view/account_journal.xml',
        'views/sale_order_quotation_dz.xml',
        'views/invoice_order_dz.xml',

    ],
    'demo': [

             ],
    'auto_install': False,
    'installable': True,
   # 'images': [],
}
