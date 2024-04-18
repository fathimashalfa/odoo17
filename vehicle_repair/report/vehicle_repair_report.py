# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class VehicleReport(models.AbstractModel):
    """This class is for Vehicle  report"""
    _name = "report.vehicle_repair.report_vehicle_repair"
    _description = "Vehicle Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        print('data', data)
        return {
            'data': data,
        }
