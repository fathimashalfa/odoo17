# -*- coding: utf-8 -*-

{
    'name': "Absentees",
    'version': '17.0.0.0',
    'depends': ['base', 'hr_attendance', 'hr'],
    'author': "shalfa",
    'category': 'Category',
    'description': """
    absentees list
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/absentees_views.xml',
        'data/absentees_sheduled_action.xml',

    ],

    'installable': True,
    'auto_install': False
}
