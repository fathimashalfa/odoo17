# -*- coding: utf-8 -*-
{
    'name': "POS Session discount",
    'version': '17.0.0.0',
    'depends': ['base','point_of_sale',],
    'author': "shalfa_p",
    'category': 'Category',
    'description': """
    Session wise maximum discount limit on pos settings
    """,
    # data files always loaded at installation
    'data': [
        'views/res_config_settings_views.xml',
        # 'views/product_card_view.xml',
        # 'views/manufacture_portal_templates.xml',

    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_session_discount/static/src/js/session_discount.js',

        ],
    },

    'installable': True,
    'auto_install': False
}