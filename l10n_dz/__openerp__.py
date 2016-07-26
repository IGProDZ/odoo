# -*- coding: utf-8 -*-
# (c) 2016 - IgPro
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Algeria - Accounting",
    "version": "8.0.0.0.0",
    "category": "Localization/Account Charts",
    "license": "AGPL-3",
    "author": "IGPro",
    "website": "http://igpro-online.net/",
    "contributors": [
        "1 <>",
        "2 <>",
        "3 <>",

    ],
    "depends": [
        "account", "account_chart",
    ],
    "data": [
        "security/ir.model.access.csv",
        "l10n_dz_wizard.xml",
        "l10n_dz_view.xml",

        "data/dz_wilayas.xml",
        "data/commune.xml",
        "data/dz_plan_comptable_normalise.xml",
        "data/dz_pcg_taxes.xml",
        "data/dz_tax.xml",
        "dz_form_juridique.xml",
        "dz_bank.xml"

    ],
    "installable": True,
    "auto_install": False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
