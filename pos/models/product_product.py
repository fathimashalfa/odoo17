# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductProduct(models.Model):
    """added a new field to translate product name to spanish """
    _inherit = "product.product"
    _translate = False

    spanish_name = fields.Char(string='Spanish Name')

