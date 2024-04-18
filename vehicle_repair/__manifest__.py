# -*- coding: utf-8 -*-

{
    'name': "Vehicle Repair Management",
    'version': '17.0.0.0',
    'depends': ['base','fleet','hr','hr_hourly_cost','product','contacts','stock','account'],
    'author': "shalfa",
    'category': 'Category',
    'description': """
    Vehicle Repair Management
    """,
    # data files always loaded at installation
    'data': [
        'security/vehicle_repair_user_group.xml',
        'security/ir.model.access.csv',
        'security/vehicle_repair_security.xml',
        'data/sequence.xml',
        'data/vehicle_type.xml',
        'data/product_data.xml',
        'views/vehicle_repair.xml',
        'views/repair_tag.xml',
        'views/res_partner.xml',
        'data/mail_template_data.xml',
        'data/archive_cancelled_record.xml',
        'data/automation_server_action.xml',
        'data/my_automation.xml',
        'wizard/vehicle_repair_wizard_views.xml',
        'report/vehicle_repair_report_views.xml',
        'report/vehicle_repair_template.xml'
       ,

    ],
    'assets':{
        'web.assets_backend':[
            'vehicle_repair/static/src/js/action_manager.js',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
