# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG

{
    'name': "Fieldservice from Sale Order",
    'summary': """
        So you can make a quotation for many fieldservice tasks and invoice them from only one sales order. A very convenience solution for your customers that have many field service tasks.
    """,
    'description': """
        odoo project management allows you to configure a service product to generate a project with timesheet entries on tasks, analytic account and sales orderline on sales order (SO) for invoicing.

        In odoo fieldservice you can not do that. odoo fieldservice has it’s own task and invoicing works with the option saleorder from task. That means, each fieldservice task needs a sale order.

        The module “Fieldservice from Salesorder” offers you the possibility to create a service product to:
        -	put on sale orderline (SO), confirm sales order
        -	generate a analytic account
        -	generate a fieldservice project
        -	generate a fieldservice task on this project
        -	to invoice timesheet entries directly from salesorder
        
        So you can make a quotation for many fieldservice tasks and invoice them from only one sales order. A very convenience solution for your customers that have many field service tasks.

    """,
    'author': "giordano.ch AG",
    'website': "http://www.giordano.ch",
    'license': 'LGPL-3',
    'currency': 'EUR',
    'price': 150.00,
    'images': ['static/description/logo_big.png'],
    'category': 'Products',
    'version': '13.0.1.0.1',
    'depends': ['base',
                'sale',
                'product',
                'stock',
                'stock_account',
                'purchase',
                'industry_fsm',
                'sale_timesheet',
                ],
    'data': [
        'views/gio_project_task_view.xml'
    ],
}