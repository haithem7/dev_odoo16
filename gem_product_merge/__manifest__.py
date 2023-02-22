# -*- coding: utf-8 -*-
{
    'name': "marge-product",

    'summary': """
        add margin based of last purchase price and standard price""",

    'description': """
        add margin based of last purchase price and standard price""",

    'author': "Haithem",
    'website': "https://www.haithemdahech.com",

    'category': 'sale',
    'version': '16.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
}
