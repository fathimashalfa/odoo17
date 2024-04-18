
{
    'name': "PDF demo",
    'version': '17.0',
    'depends': ['base','web','sale_management','stock'],
    'author': "shalfa",
    'category': 'Sales',
    'description': """
    PDF Technical session
    """,
    # data files always loaded at installation
    'data': [
        'data/paper_paper_format.xml',
        'report/report_layout.xml',
        'report/demo_report_template.xml',


    ],
    'external_dependencies':{
        'python':['matplotlib'],

    },

    'license' : 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
