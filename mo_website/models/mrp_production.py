# -*- coding: utf-8 -*-
from odoo import fields, models


class MrpProduction(models.Model):
    """added a new field for customer"""
    _inherit = 'mrp.production'

    customer_id = fields.Many2one(string="Customer", comodel_name='res.partner')
