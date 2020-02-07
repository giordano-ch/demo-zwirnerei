# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG

from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'account.move.line'


    @api.depends('product_id')
    @api.onchange('product_id')
    def onchange_product_id_changes(self):
        if self.product_id:
            self.analytic_tag_ids = self.product_id.gio_analytic_tag
            self.analytic_account_id = self.product_id.gio_analytic_account