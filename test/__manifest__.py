{
    'name': 'Test',
    'version': '1.0',
    'category': 'Test',
    'sequence': 15,
    'summary': 'Test Module',
    'website': 'trescloud.com',
    'depends': [
        'base',
        'sale', 
        'stock',
        'account',
    ],
    'data': [
        # Security files (ALWAYS FIRST)
        'security/delivery_detail_security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/delivery_detail_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}