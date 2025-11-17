# -- coding: utf-8 --
{
    'name': "TailorStyle Website",
    'version': "1.0",
    'summary': "Customer frontend for TailorStyle",
    'description': """
        TailorStyle Website Module
        - Home page
        - Collections page
        - Customer registration
        - Customer orders
        - Order tracking
    """,
    'author': "Your Name",
    'category': "Website",
    'depends': ['base', 'web', 'website', 'tailorstyle_management'],  # depends on your backend module
    'data': [
        'views/home_page.xml',
        'views/collections_page.xml',
        'views/order_page.xml',
        'views/orders_page.xml',
        'views/registration_page.xml',
        'views/templates.xml',
        'views/user_login.xml',
        'views/user_not_found.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tailorstyle_website/static/src/css/style.css',
            'tailorstyle_website/static/src/js/script.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}