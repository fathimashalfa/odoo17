# -*- coding: utf-8 -*-
{
    'name': "POS Product",
    'version': '17.0.0.0',
    'depends': ['base','product','point_of_sale',],
    'author': "shalfa_p",
    'category': 'Category',
    'description': """
    Spanish Product name in POS
    """,
    # data files always loaded at installation
    'data': [
        'views/product_templates_views.xml',
        # 'views/product_card_view.xml',
        # 'views/manufacture_portal_templates.xml',

    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos/static/src/xml/product_card_view.xml',
            'pos/static/src/xml/order_receipt.xml',
            'pos/static/src/xml/product_list.xml',
            'pos/static/src/js/load_field.js',
            'pos/static/src/js/product_card_view.js',
        ],
    },

    'installable': True,
    'auto_install': False
}