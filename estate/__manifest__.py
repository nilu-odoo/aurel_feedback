# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Estate",
    'application': True,
    'depends': ['base'],
    'installable' : True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',

}