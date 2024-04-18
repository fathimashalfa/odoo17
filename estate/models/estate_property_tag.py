from odoo import fields, models


class Estate_Property_tag(models.Model):
    _name = "estate.property.tag"

    name = fields.Char(required=True, string="Name")



# def generate_xlsx_report(self):
#     # self.get_query()
#     report = self.env.cr.dictfetchall()
#     count = len(self.customer_ids)
#     adv_count = len(self.service_advisor_ids)
#     data = {'date': self.read()[0], 'report': report, 'count': count, 'adv_count': adv_count,
#             'group_by': self.group_by}
#     return {
#         'type': 'ir.actions.report',
#         'data': {'model': 'repair.wizard',
#                  'options': json.dumps(data,
#                                        default=date_utils.json_default),
#                  'output_format': 'xlsx',
#                  'report_name': 'Repair Excel Report',
#                  },
#         'report_type': 'xlsx',
#     }
#
# def get_xlsx_report(self, data, response):
#     output = io.BytesIO()
#     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
#     sheet = workbook.add_worksheet()
#     sheet.set_column('B:L', 18)
#     cell_format = workbook.add_format(
#         {'font_size': '12px', 'align': 'center'})
#     head = workbook.add_format(
#         {'align': 'center', 'bold': True, 'font_size': '20px'})
#     txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
#
#     if data['count'] == 1 and data['report']:
#         customer_data = data['date'].get('customer_ids')
#         if customer_data and isinstance(customer_data, list) and len(customer_data) > 0:
#             sheet.merge_range('B4:C4', data['report'][0]['name'], cell_format)
#     if data['adv_count'] == 1 and data['report']:
#         adv_data = data['date'].get('service_advisor_ids')
#         if adv_data and isinstance(adv_data, list) and len(adv_data) > 0:
#             sheet.merge_range('B5:C5', data['report'][0]['user_name'], cell_format)
#     if data['group_by'] == 'service_type':
#         sheet.write('E6', 'Service Type', cell_format)
#
#         if data['date'].get('group_by') == 'service_type':
#             data['service_types'] = ['paid', 'free']
#         i = 6
#         sheet.merge_range('B2:I3', 'REPAIR REPORT', head)
#         for rec in data['service_types']:
#             sheet.write(f'B{i}', 'Vehicle Model', cell_format)
#             sheet.write(f'C{i}', 'Vehicle Number', cell_format)
#             if data.get('count') < 1:
#                 sheet.write(f'D{i}', 'Customer', cell_format)
#             if data.get('adv_count') < 1:
#                 sheet.write(f'E{i}', 'Service Advisors', cell_format)
#                 sheet.write(f'F{i}', 'Start Date', cell_format)
#                 sheet.write(f'G{i}', 'End Date', cell_format)
#                 sheet.write(f'H{i}', 'State', cell_format)
#                 sheet.write(f'I{i}', 'Estimate Amount', cell_format)
#                 sheet.write(f'J{i}', 'Total Amount', cell_format)
#                 sheet.write(f'K{i}', 'Vehicle Type', cell_format)
#             else:
#                 sheet.write(f'D{i}', 'Start Date', cell_format)
#                 sheet.write(f'E{i}', 'End Date', cell_format)
#                 sheet.write(f'F{i}', 'State', cell_format)
#                 sheet.write(f'G{i}', 'Estimate Amount', cell_format)
#                 sheet.write(f'H{i}', 'Total Amount', cell_format)
#                 sheet.write(f'I{i}', 'Vehicle Type', cell_format)
#
#             j = i + 2
#             for vehicle in (data['report']):
#                 if rec == vehicle['service_type']:
#                     B7 = i + 1
#                     sheet.write(f'B{j}', vehicle['fleet'], cell_format)
#                     sheet.write(f'C{j}', vehicle['vehicle_number'], cell_format)
#                     if data.get('count') < 1:
#                         sheet.write(f'D{j}', vehicle['name'], cell_format)
#                     if data.get('adv_count') < 1:
#                         sheet.write(f'E{j}', vehicle['user_name'], cell_format)
#                         sheet.write(f'F{j}', vehicle['start_date'], cell_format)
#                         sheet.write(f'G{j}', vehicle['due_date'], cell_format)
#                         sheet.write(f'H{j}', vehicle['state'], cell_format)
#                         sheet.write(f'I{j}', vehicle['estimated_amount'], cell_format)
#                         sheet.write(f'J{j}', vehicle['total_cost'], cell_format)
#                         sheet.write(f'B{B7}', vehicle['service_type'], cell_format)
#                         sheet.write(f'K{j}', vehicle['vehicle'], cell_format)
#                         j += 1
#
#                     else:
#                         sheet.write(f'D{j}', vehicle['start_date'], cell_format)
#                         sheet.write(f'E{j}', vehicle['due_date'], cell_format)
#                         sheet.write(f'F{j}', vehicle['state'], cell_format)
#                         sheet.write(f'G{j}', vehicle['estimated_amount'], cell_format)
#                         sheet.write(f'H{j}', vehicle['total_cost'], cell_format)
#                         sheet.write(f'I{j}', vehicle['vehicle'], cell_format)
#                         j += 1
#             i = j + 2
#
#     else:
#         if data['group_by'] == 'vehicle_type_id':
#             sheet.write('E6', 'Vehicle Type', cell_format)
#             if data['date'].get('group_by') == 'vehicle_type_id':
#                 datass = self.env['fleet.vehicle.model.category'].sudo().search([])
#                 data['vehicle_types'] = datass.mapped('name')
#                 i = 6
#                 sheet.merge_range('B2:I3', 'REPAIR REPORT', head)
#
#                 for rec in data['vehicle_types']:
#                     if len(list(filter(lambda x: x['vehicle'] == rec, data['report']))):
#                         sheet.write(f'B{i}', 'Vehicle Model', cell_format)
#                         sheet.write(f'C{i}', 'Vehicle Number', cell_format)
#                         if data.get('count') < 1:
#                             sheet.write(f'D{i}', 'Customer', cell_format)
#                         if data.get('adv_count') < 1:
#                             sheet.write(f'E{i}', 'Service Advisors', cell_format)
#                             sheet.write(f'F{i}', 'Start Date', cell_format)
#                             sheet.write(f'G{i}', 'End Date', cell_format)
#                             sheet.write(f'H{i}', 'State', cell_format)
#                             sheet.write(f'I{i}', 'Estimate Amount', cell_format)
#                             sheet.write(f'J{i}', 'Total Amount', cell_format)
#                             sheet.write(f'K{i}', 'Service Type', cell_format)
#                         else:
#                             sheet.write(f'D{i}', 'Start Date', cell_format)
#                             sheet.write(f'E{i}', 'End Date', cell_format)
#                             sheet.write(f'F{i}', 'State', cell_format)
#                             sheet.write(f'G{i}', 'Estimate Amount', cell_format)
#                             sheet.write(f'H{i}', 'Total Amount', cell_format)
#                             sheet.write(f'I{i}', 'Service Type', cell_format)
#
#                         j = i + 2
#
#                         for vehicle in (data['report']):
#                             if rec == vehicle['vehicle']:
#                                 B7 = i + 1
#                                 sheet.write(f'B{j}', vehicle['fleet'], cell_format)
#                                 sheet.write(f'C{j}', vehicle['vehicle_number'], cell_format)
#                                 if data.get('count') < 1:
#                                     sheet.write(f'D{j}', vehicle['name'], cell_format)
#                                 if data.get('adv_count') < 1:
#                                     sheet.write(f'E{j}', vehicle['user_name'], cell_format)
#                                     sheet.write(f'F{j}', vehicle['start_date'], cell_format)
#                                     sheet.write(f'G{j}', vehicle['due_date'], cell_format)
#                                     sheet.write(f'H{j}', vehicle['state'], cell_format)
#                                     sheet.write(f'I{j}', vehicle['estimated_amount'], cell_format)
#                                     sheet.write(f'J{j}', vehicle['total_cost'], cell_format)
#                                     sheet.write(f'K{j}', vehicle['service_type'], cell_format)
#                                     sheet.write(f'B{B7}', vehicle['vehicle'], cell_format)
#                                     j += 1
#
#                                 else:
#                                     sheet.write(f'D{j}', vehicle['start_date'], cell_format)
#                                     sheet.write(f'E{j}', vehicle['due_date'], cell_format)
#                                     sheet.write(f'F{j}', vehicle['state'], cell_format)
#                                     sheet.write(f'G{j}', vehicle['estimated_amount'], cell_format)
#                                     sheet.write(f'H{j}', vehicle['total_cost'], cell_format)
#                                     sheet.write(f'I{j}', vehicle['service_type'], cell_format)
#                                     j += 1
#                         i = j + 2
#     workbook.close()
#     output.seek(0)
#     response.stream.write(output.read())
#     output.close()