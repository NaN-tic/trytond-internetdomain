#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Internet Domain',
    'name_ca_ES': 'Dominis internet',
    'name_es_ES': 'Dominios internet',
    'version': '2.4.0',
    'author': 'Zikzakmedia',
    'email': 'zikzak@zikzakmedia.com',
    'website': 'http://www.zikzakmedia.com/',
    'description': '''Internet Domain Management. Domains and renewals.
''',
    'description_ca_ES': '''Gestió de dominis internet. Dominis i renovacions.
''',
    'description_es_ES': '''Gestión de dominios de internet. Dominios y renovaciones.
''',
    'depends': [
        'ir',
        'res',
        'company',
        'party',
        'product',
    ],
    'xml': [
        'company.xml',
        'internetdomain.xml',
    ],
    'translation': [
        'locale/ca_ES.po',
        'locale/es_ES.po',
    ]
}
