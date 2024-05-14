# -*- coding: utf-8 -*-
from odoo import fields, models


class Website(models.Model):
    """added the field to website model"""
    _inherit = 'website'

    multiple_prod_ids = fields.Many2many(comodel_name="mrp.bom")


class ResConfigSettings(models.TransientModel):
    """field to add multiple products in settings """
    _inherit = 'res.config.settings'

    multiple_prod_ids = fields.Many2many(
        related='website_id.multiple_prod_ids',
        comodel_name='mrp.bom',
        readonly=False)
