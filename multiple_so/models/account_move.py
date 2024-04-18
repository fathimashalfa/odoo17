# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountMove(models.Model):
    """field Needed to select multiple sale order"""
    _inherit = 'account.move'

    related_so_ids = fields.Many2many(comodel_name='sale.order', string="Related SO")

    @api.onchange('related_so_ids')
    def _onchange_related_so_ids(self):
        """Selected Sales Order's Order lines should be added to the invoice lines"""
        # self.invoice_line_ids = [fields.Command.clear()]
        self.update({
            'invoice_line_ids': [fields.Command.clear()]
        })
        for record in self.related_so_ids.order_line:
            self.update({
                'invoice_line_ids': [fields.Command.create({
                    'product_id': record.product_id.id,
                    'name': record.product_id.name,
                    'quantity': record.product_uom_qty,
                    'price_unit': record.price_unit,
                    'display_type': 'product',
                    'sale_line_ids': [fields.Command.link(record._origin.id)]
                })]
            })
            # self.env["account.move.line"].create({
            #     'product_id': record.product_id.id,
            #     'name': record.product_id.name,
            #     'quantity': record.product_uom_qty,
            #     'price_unit': record.price_unit,
            #     'display_type': 'product',
            #     'sale_line_ids': [fields.Command.link(record._origin.id)],
            #     'move_id': self._origin.id
            # })
                # record.update({'invoice_lines': [(4, [record.id])]})


class AML(models.Model):
    _inherit = "account.move.line"
    
    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        return super().create(vals_list)