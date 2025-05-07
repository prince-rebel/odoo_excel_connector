# -*- coding: utf-8 -*-
{
    'name': 'Créances Clients API',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Expose une API REST pour les créances clients (Odoo 10)',
    'description': 'Permet de récupérer les créances clients pour Power Query/Excel via une API JSON',
    'author': 'Djakaridja Traore',
    'depends': ['account'],
    'data': ['views/res_users_view.xml'],
    'installable': True,
    'application': False,
}
