# -*- coding: utf-8 -*-

{
    'name': "BOM Cart",
    'version': '17.0.0.0',
    'depends': ['base','website', 'website_sale', 'mrp','sale_management'],
    'author': "shalfa_p",
    'category': 'Category',
    'description': """
    BILL OF MATERIAL CART
    """,
    'data': [
        'views/res_config_settings_views.xml',
        'views/templates_bom.xml',

    ],

    'installable': True,
    'auto_install': False
}
