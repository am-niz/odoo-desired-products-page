# -*- coding: utf-8 -*-
{
    'name': "Desired Products",

    'summary': "Adding an additional page Initial Products ",

    'description': """
Adding an additional page Initial Products after the Order Lines of sale_order model and sale_order_reports and also on 
invoice page as well as invoice reports
    """,

    'author': "NIZAMUDHEEN MJ",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'account', 'l10n_in'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_desired_views.xml',
        'views/account_desired_views.xml',
        'reports/sale_desired_report.xml',
        'reports/invoice_desired_report.xml',
    ],
    "application": True,
    "sequence": -94,
    # only loaded in demonstration mode

}

