# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Fields Require to set Discount Limit"""
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Discount limit Approval", config_parameter="discount_limit.so_order_approval",
                                       default=lambda self: self.env.company.po_double_validation == 'two_step')

    po_double_validation = fields.Selection(
        related='company_id.po_double_validation', string="Levels of Approvals *",
        readonly=False)
    po_double_validation_amount = fields.Monetary(
        related='company_id.po_double_validation_amount',
        string="Minimum Amount", currency_field='company_currency_id',
        readonly=False)
    company_currency_id = fields.Many2one('res.currency', config_parameter="discount_limit.company_currency_id"
                                          , string="Company Currency",
                                          readonly=True)

