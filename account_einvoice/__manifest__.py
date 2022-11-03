# -*- coding: utf-8 -*-

{
    'name': 'Account Invoice electronic Peru',
    'version': '14.0.12',
    'category': 'Accounting & Finance',
    'description': """

Account Invoice electronic.
===========================
This application add new fields on the account invoice model.

    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': [
        'account',
        'sunat_document_type',
        'l10n_pe_base',
        'res_partner_peru',
        'rapitech_account_advance'
        #'sale'
    ],
    'data': [
        'data/catalog_7_data.xml',
        'data/catalog_8_data.xml',
        'data/catalog_9_data.xml',
        'data/catalog_10_data.xml',
        'security/ir.model.access.csv',
        #'wizard/account_invoice_refund_view.xml',
        'views/invoice_form.xml',
        
    ],
    'installable': True,
    'auto_install': False,
}
