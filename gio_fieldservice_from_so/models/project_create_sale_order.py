# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProjectCreateSalesOrder(models.TransientModel):
    _inherit = 'project.create.sale.order'


    def _create_sale_order(self):
        """ Private implementation of generating the sales order """
        sale_order = self.env['sale.order'].create({
            'project_id': self.project_id.id,
            'partner_id': self.partner_id.id,
            'analytic_account_id': self.project_id.analytic_account_id.id,
            'client_order_ref': self.project_id.name,
            'company_id': self.project_id.company_id.id,
        })
        sale_order.onchange_partner_id()
        sale_order.onchange_partner_shipping_id()

        # create the sale lines, the map (optional), and assign existing timesheet to sale lines
        self._make_billable(sale_order)

        # confirm SO
        sale_order.action_confirm()
        return sale_order

    def _make_billable(self, sale_order):
        if self.billable_type == 'project_rate':
            self._make_billable_at_project_rate(sale_order)
        else:
            self._make_billable_at_employee_rate(sale_order)


    def _make_billable_at_project_rate(self, sale_order):
        # trying to simulate the SO line created a task, according to the product configuration
        # To avoid, generating a task when confirming the SO
        task_id = False
        if self.product_id.service_tracking in ['task_in_project', 'task_global_project', 'gio_fieldservice_task']:
            task_id = self.env['project.task'].search([('project_id', '=', self.project_id.id)], order='create_date DESC', limit=1).id

        # create SO line
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id,
            'product_uom_qty': 0.0,
        })

        # link the project and the tasks to the SO line
        self.project_id.write({
            'sale_order_id': sale_order.id,
            'sale_line_id': sale_order_line.id,
            'partner_id': self.partner_id.id,
        })
        self.project_id.tasks.filtered(lambda task: task.billable_type == 'no').write({
            'sale_line_id': sale_order_line.id,
            'partner_id': sale_order.partner_id.id,
            'email_from': sale_order.partner_id.email,
        })

        # assign SOL to timesheets
        self.env['account.analytic.line'].search([('task_id', 'in', self.project_id.tasks.ids), ('so_line', '=', False)]).write({
            'so_line': sale_order_line.id
        })

        return sale_order_line


    def _make_billable_at_employee_rate(self, sale_order):
        # trying to simulate the SO line created a task, according to the product configuration
        # To avoid, generating a task when confirming the SO
        task_id = self.env['project.task'].search([('project_id', '=', self.project_id.id)], order='create_date DESC', limit=1).id
        project_id = self.project_id.id

        non_billable_tasks = self.project_id.tasks.filtered(lambda task: task.billable_type == 'no')

        map_entries = self.env['project.sale.line.employee.map']
        EmployeeMap = self.env['project.sale.line.employee.map'].sudo()

        # create SO lines: create on SOL per product/price. So many employee can be linked to the same SOL
        map_product_price_sol = {}  # (product_id, price) --> SOL
        for wizard_line in self.line_ids:
            map_key = (wizard_line.product_id.id, wizard_line.price_unit)
            if map_key not in map_product_price_sol:
                values = {
                    'order_id': sale_order.id,
                    'product_id': wizard_line.product_id.id,
                    'price_unit': wizard_line.price_unit,
                    'product_uom_qty': 0.0,
                }
                if wizard_line.product_id.service_tracking in ['task_in_project', 'task_global_project', 'gio_fieldservice_task']:
                    values['task_id'] = task_id
                if wizard_line.product_id.service_tracking in ['task_in_project', 'project_only', 'gio_fieldservice_task']:
                    values['project_id'] = project_id

                sale_order_line = self.env['sale.order.line'].create(values)
                map_product_price_sol[map_key] = sale_order_line

            map_entries |= EmployeeMap.create({
                'project_id': self.project_id.id,
                'sale_line_id': map_product_price_sol[map_key].id,
                'employee_id': wizard_line.employee_id.id,
            })

        # link the project to the SO
        self.project_id.write({
            'sale_order_id': sale_order.id,
            'sale_line_id': sale_order.order_line[0].id,
            'partner_id': self.partner_id.id,
        })
        non_billable_tasks.write({
            'sale_line_id': sale_order.order_line[0].id,
            'partner_id': sale_order.partner_id.id,
            'email_from': sale_order.partner_id.email,
        })

        # assign SOL to timesheets
        for map_entry in map_entries:
            self.env['account.analytic.line'].search([('task_id', 'in', self.project_id.tasks.ids), ('employee_id', '=', map_entry.employee_id.id), ('so_line', '=', False)]).write({
                'so_line': map_entry.sale_line_id.id
            })

        return map_entries