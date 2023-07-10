# -*- coding: utf-8 -*-
{
    'name': "Firebase Service",

    'summary': """
        Modulo de servicios para las notificaciones push utilizando el modulo de servicios
        de Cloud Messaging""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Universidad Politecnica Salesiana",
    'website': "https://www.ups.edu.ec",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Marketing/Email Marketing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','loyalty','point_of_sale'],  # Dependencias del módulo
    'external_dependencies': {
            'python': ['firebase_admin'],
        },
    'installable': True,
    'application': True,
    'auto_install': False,
    # always loaded
    'data': [
        'views/firebase_notification_views.xml',
        'views/res_partner_inherit.xml',
        'security/ir.model.access.csv',
    ],

}
