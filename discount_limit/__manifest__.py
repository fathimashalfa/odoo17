# -*- coding: utf-8 -*-

{
    'name': "Discount",
    'version': '17.0.0.0',
    'depends': ['base','sale_management'],
    'author': "shalfa_p",
    'category': 'Category',
    'description': """
    Discount limit
    """,
    # data files always loaded at installation
    'data': [
        'views/res_config_settings_views.xml',
        'views/sale.order.xml',
        # 'views/estate_property_tag.xml',

    ],

    'installable': True,
    'auto_install': False
}
