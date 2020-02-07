# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"


    gio_analytic_account = fields.Many2one('account.analytic.account', string="ANALYTIC ACCOUNT")
    gio_analytic_tag = fields.Many2one('account.analytic.tag', string="ANALYTIC TAG", copy=False)