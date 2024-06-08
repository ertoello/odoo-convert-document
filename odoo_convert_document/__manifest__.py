# -*- coding: utf-8 -*-
{
    'name': "odoo_convert_document",

    'summary': """
        This module has been integrated with the API from the https://www.convertapi.com website""",

    'description': """
        Converting Document in Odoo 16
    """,

    'author': "Yohanes Serpiyanto Elo",
    'website': "https://github.com/ertoello",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence.xml',
        'views/convert_views.xml',
        'views/api_setting_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
