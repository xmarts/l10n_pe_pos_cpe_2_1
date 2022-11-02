# -*- coding: utf-8 -*-
{
    'name': "Peruvian POS",

    'summary': """
        Peruvian Management POS""",

    'description': """
        Peruvian Management POS
    """,

    'author': "Rapid Technologies SAC",
    'website': "http://www.rapi.tech",
    'category': 'POS PERU',
    'version': '0.30',

    'depends': [
        'point_of_sale',
        'l10n_pe_pos_2_1',
        'account_einvoice',
    ],

    'data': [
        'views/pos_config_view.xml',
        'views/l10n_pe_pos_templates.xml',
        'data/data.xml',
        'views/report.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'installable': True,
}
