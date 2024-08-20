# -*- coding: utf-8 -*-
{
    'name': "Iphonebali",

    'summary': """
        Iphonebali website, ecommerce, and product management""",

    'description': """
         Iphonebali website, ecommerce, and product management""",

    'author': "Steven",

    'category': 'Uncategorized',
    'version': '1.0',
    'application': True,
    'installable': True,


    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/product_type_views.xml',
        'views/product_tag_views.xml',
        'views/product_offer_views.xml'
    ],
}
