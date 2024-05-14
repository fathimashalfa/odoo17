# -*- coding: utf-8 -*-
from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    discount_active = fields.Boolean(string='Session Discount')
    session_name = fields.Many2many(string="Session", comodel_name='pos.session')
    discount_limit = fields.Selection([('fixed_amount', 'Fixed Amount'),
                                       ('percentage', 'Percentage(%)')], default="fixed_amount", required=True,
                                      help="Choose the session Discount")
    discount = fields.Float(string='Discount')


class ResConfigSettings(models.TransientModel):
    """field to set session wise discount limit in POS settings """
    _inherit = 'res.config.settings'

    pos_discount_limit = fields.Selection(related="pos_config_id.discount_limit", readonly=False)
    pos_discount_active = fields.Boolean(related="pos_config_id.discount_active", readonly=False)
    pos_discount = fields.Float(related="pos_config_id.discount", readonly=False)
    pos_session_name = fields.Many2many(related='pos_config_id.session_name', readonly=False)
