
{
    'name': "Real Estate",
    'version': '17.0',
    'depends': ['base'],
    'author': "shalfa",
    'category': 'Category',
    'description': """
    Real estate app
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_view.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
