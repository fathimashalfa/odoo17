# -*- coding: utf-8 -*-
import io
import xlsxwriter
from odoo import fields, models
from odoo.exceptions import ValidationError, UserError
import json
from odoo.tools import date_utils


class VehicleRepairWizard(models.TransientModel):
    """This model is used for sending WhatsApp messages through Odoo."""
    _name = 'vehicle.repair.wizard'
    _description = "Vehicle Repair Wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End date")
    partner_ids = fields.Many2many(string="Customer", comodel_name='res.partner', store=True)
    service_advisor_ids = fields.Many2many(string='Service Advisor', comodel_name='res.users', store=True)

    grouping_method = fields.Selection([
        ('service_type', 'Service Type'),
        ('vehicle_type', 'Vehicle Type')
    ], string='Group By', default='service_type', required=True)

    def _check_to_date_from_date(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("From date must be less than to date")

    def get_query(self):
        query = """SELECT vehicle_model_id,
                vr.partner_id,
                vehicle_number,
                service_advisor_id,
                estimated_amount,
                sum_labour_component_cost as total_amount,
                vr.state,
                start_date,
                delivery_date,
                vehicle_type_id,
                Service_type,
                fm.name as vehicle_model,
                fc.name as vehicle_type,
                pr.name as customer,
                p.name as user
                from vehicle_repair as vr
                left join fleet_vehicle_model as fm on fm.id = vr.vehicle_model_id 
                left join fleet_vehicle_model_category as fc on fc.id = vr.vehicle_type_id
                left join res_partner as pr on pr.id = vr.partner_id
                left join res_users as ur on ur.id = vr.service_advisor_id
                left join res_partner as p on p.id = ur.partner_id 
                where 1=1"""

        if self.start_date:
            query += """ AND vr.start_date = '%s' """ % self.start_date

        if self.end_date:
            query += """ AND vr.delivery_date = '%s' """ % self.end_date

        if self.service_advisor_ids:
            user_tup = tuple(self.service_advisor_ids.mapped('name'))
            if len(user_tup) == 1:
                query += f""" AND p.name = '{str(user_tup[0])}'"""

        #
        if self.partner_ids:
            partners = tuple([x.id for x in self.partner_ids]) if len(self.partner_ids) > 1 else self.partner_ids.id
            query += f"""AND vr.partner_id in {partners}""" if len(
                self.partner_ids) > 1 else f"""AND vr.partner_id = {partners}"""

        if query:
            self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_pdf_report(self):
        self._check_to_date_from_date()
        report = self.get_query()
        customer_count = len(self.partner_ids)
        service_advisor_count = len(self.service_advisor_ids)
        data = {
            'report': report,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'partner_id': self.partner_ids.mapped('name'),
            'service_advisor_id': self.service_advisor_ids.mapped('partner_id'),
            'grouping_method': self.grouping_method,
            'customer_count': customer_count,
            'service_advisor_count': service_advisor_count,
        }
        if report:
            return self.env.ref('vehicle_repair.action_vehicle_repair_report').report_action(None, data=data)
        else:
            raise UserError("Please check your credentials!!!")

    def action_xlsx_report(self):
        print("huuvurbuybvubvubuhvbubvh")
        self._check_to_date_from_date()
        report = self.get_query()
        counts = self.action_pdf_report()
        customer_count = len(self.partner_ids)
        service_advisor_count = len(self.service_advisor_ids)

        data = {
            'report': report,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'partner_id': self.partner_ids.mapped('name'),
            'service_advisor_id': self.service_advisor_ids.mapped('partner_id'),
            'grouping_method': self.grouping_method,
            'customer_count': customer_count,
            'service_advisor_count': service_advisor_count
        }
        print("data", data)
        print(data['grouping_method'])
        print("report", report)
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'vehicle.repair.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'vehicle Excel Report',
                         },
                'report_type': 'xlsx',

            }
        else:
            UserError("Check your Credentials")

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.set_column('B:Q', 18)
        sheet.merge_range('B2:I3', ' VEHICLE EXCEL REPORT', head)
        if data.get('customer_count') == 1:
            if data['report']:
                sheet.write('C6', 'Customer:', cell_format)
                sheet.write('D6', data['report'][0]['customer'], txt)
        if data.get('service_advisor_count') == 1:
            if data['report']:
                sheet.write('G6', 'Service Advisor:', cell_format)
                sheet.write('H6', data['report'][0]['user'], txt)
        if data['grouping_method'] == 'service_type':
            sheet.merge_range('C8:H9', 'SERVICE TYPE', cell_format)
        if data['grouping_method'] == 'vehicle_type':
            sheet.merge_range('C8:H9', 'VEHICLE TYPE', cell_format)
            


        # sheet.write('B9', 'Vehicle Model', cell_format)
        # sheet.write('C9', 'Vehicle Number', cell_format)
        # sheet.write('D9', 'Start date', cell_format)
        # if data['start_date']:
        #     strt = data['start_date']
        # else:
        #     strt = ''
        # sheet.write('D10', strt, txt)
        # sheet.write('E9', 'End date', cell_format)
        # end = ''
        # if data['end_date']:
        #     end = data['end_date']
        # sheet.write('E10', end, txt)
        # sheet.write('F9', 'State', cell_format)
        # sheet.write('G9', 'Estimated Amount', cell_format)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
