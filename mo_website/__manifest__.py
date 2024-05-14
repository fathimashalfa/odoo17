# -*- coding: utf-8 -*-

{
    'name': "Manufacturing Order Website",
    'version': '17.0.0.0',
    'depends': ['base','mrp','portal'],
    'author': "shalfa_p",
    'category': 'Category',
    'description': """
    Manufacturing order website
    """,
    # data files always loaded at installation
    'data': [
        'views/mrp_orders_views.xml',
        'views/portal_templates.xml',
        'views/manufacture_portal_templates.xml',

    ],

    'installable': True,
    'auto_install': False
}
