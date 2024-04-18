# -*- coding: utf-8 -*-

{
    'name': "Multiple Saleorder Invoice",
    'version': '17.0.0.0',
    'depends': ['base','account','sale_management'],
    'author': "shalfa_p",
    'category': 'Category',
    'description': """
    Multiple Saleorder Invoice
    """,
    # data files always loaded at installation
    'data': [
        'views/account_move_views.xml',

    ],

    'installable': True,
    'auto_install': False
}
