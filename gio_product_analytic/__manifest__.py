# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG

{
    'name': "Analytic Account and Analytic Tag on Product (SO/CI and PO/VB)",
    'summary': """
       Product
        Automate the use of analytic account and analytic tag - save analytic account and analytic tag on a product. 
    """,
    'description': """
        Product
    Automate the use of analytic account and analytic tag - save analytic account and analytic tag on a product. 
    Sale Order and Customer Invoice
    Add this product to a sale order line, analytic account and analytic tag will be saved within the sale order line. Form sales order you will generate the customer invoice. This module will move analytic account and analytic tag from product to the invoice line and save the amount from sale order line to analytic account with analytic tag. So you can use analytic account and analytic tag in your financial reports to analize revenues.
    Purchase Order and Vendor Bill
    Add this product to a purchase order line, analytic account and analytic tag will be saved within the purchase order line. Form purchase order you will generate the vendor bill. This module will move analytic account and analytic tag from product to the vendor bill line and save the amount from vendor bill line to analytic account with analytic tag. So you can use analytic account and analytic tag in your financial reports to analize expensis.
    """,
    'author': "giordano.ch AG",
    'website': "http://www.giordano.ch",
    'license': 'LGPL-3',
    'currency': 'EUR',
    'price': 25.00,
    'images': ['static/description/logo_big.png'],
    'category': 'Products',
    'version': '13.0.1.0.1',
    'depends': ['base',
                'sale',
                'product',
                'stock',
                'stock_account',
                'purchase',
                ],
    'data': [
        'views/gio_product_view_inherit.xml'
    ],
}