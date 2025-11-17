{
    'name': 'TailorStyle Management',
    'version': '1.0',
    'summary': 'Custom Cloth Ordering and Management System',
    'description': """
        TailorStyle - A cloth ordering website and admin panel.
        Allows customers to view and order clothes,
        and admin to manage users, cloth details, and track orders.
    """,
    'author': 'Denitta Johnson',
    'website': 'http://localhost:8069',  # you can later replace this with your live domain
    'category': 'Website',
    'depends': ['base', 'website', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/user_view.xml',
        'views/cloth_view.xml',
        'views/order_view.xml',
        'views/menus.xml',
        'data/sequence.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}