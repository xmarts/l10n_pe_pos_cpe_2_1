# -*- coding: utf-8 -*-
{
    'name': "Peruvian POS PERU",

    'summary': """
         Management POS""",

    'description': """
        Management POS PERU
    """,

    'author': "Rapid Technologies SAC",
    'website': "http://www.rapi.tech",
    'category': 'POS PERU',
    'version': '0.15',

    'depends': [
        'point_of_sale',
        'amount_to_text',
        'res_partner_peru',
        'l10n_pe_cpe',
        'point_of_sale_multi_store',
    ],

    'data': [
        'views/l10n_pe_pos_templates.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'installable': True,
}