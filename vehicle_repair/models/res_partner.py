# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_count = fields.Integer(string="Service History",
                                   compute='compute_vehicle_count')
    state = fields.Selection([
                              ('non_service_customer', 'Non Service Customer'),
                              ('service_customer', 'Service Customer'),
                              ], default="non_service_customer", help="mention the state", tracking=True)

    def action_get_vehicles_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Service History',
            'view_mode': 'tree',
            'res_model': 'vehicle.repair',
            'domain': [('partner_id', '=', self.id)],
            'context': "{'create': True}"
        }

    def compute_vehicle_count(self):
        for record in self:
            record.vehicle_count = self.env['vehicle.repair'].search_count(
                [('partner_id', '=', record.id)])

    def create_repair(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Repair',
            'view_mode': 'form',
            'res_model': 'vehicle.repair',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id}

        }

    def action_archive(self):
        records = self.env['vehicle.repair'].search([('partner_id', '=', self.id)])
        print(records, "hello")
        records.active = False
        return super().action_archive()

    def action_unarchive(self):
        records = self.env['vehicle.repair'].with_context(active_test=False).search([('partner_id', '=', self.id)])
        records.active = True
        print(records)
        return super().action_unarchive()
