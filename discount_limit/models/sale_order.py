# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    """added a ne state to sale_order"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', "To Approve"), ('sent',)])
    # move_ids = fields.Many2many(comodel_name="account.move",string="Move Id")

    #
    def button_approve(self):
        """Function to perform approve Button"""
        self.action_confirm()

    def action_confirm(self):
        """Adding new Functionalities to confirm button in sale_order for to show approve button when discount become
        greater than discount limit"""
        limit_amount = self.env.company.po_double_validation_amount
        discounts = []
        for line in self.order_line:
            if line.product_template_id.name == "Discount":
                discounts.append(abs(line.price_subtotal))
                discount_limit = sum(discounts)
            elif line.product_template_id.name != "Discount":
                discount_amounts = line.product_uom_qty * line.price_unit * line.discount / 100
                discounts.append(discount_amounts)
                discount_limit = sum(discounts)
        if discount_limit > limit_amount and self.state in ['draft', 'sent']:
            self.write({'state': 'to_approve'})
        else:
            self.write({'state': 'draft'})
            return super().action_confirm()
