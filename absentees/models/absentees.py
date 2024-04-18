# -*- coding: utf-8 -*-
import datetime

from odoo import fields, models


class Absentees(models.Model):
    """Fields require for tree view of Absentees List"""
    _name = 'absentees'

    date = fields.Date(string="Date", default=fields.Date.today())
    absentee_id = fields.Many2one(comodel_name="hr.employee", string="Employee Absent")
    email = fields.Char(related="absentee_id.work_email", string="Email")
    department_id = fields.Many2one(related="absentee_id.department_id", string="Department", store=True)

    def get_absentees_list(self):
        """ to check employee records in records of attendance in today date  """
        dates = fields.Datetime.today()
        attendance_records = self.env['hr.attendance'].search([('check_in', '<=', dates)])
        employee_records = self.env['hr.employee'].search([])
        self.create({'absentee_id': rec.id}for rec in employee_records.filtered(
            lambda rec: rec not in attendance_records.employee_id))








