# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route


class WebFormController(Controller):
    """All route and its functions deals with controller"""

    @route('/new_customer', methods=['GET'], auth='public', website=True)
    def new_customer(self, ):
        """To render the new customer creation form"""
        return request.render("vehicle_repair.new_customer_form")

    @route('/new_customer_data', methods=['POST'], auth='public', website=True)
    def customer_data(self, **kwargs):
        """passing the values filled in the new customer form to res_partner"""
        request.env['res.partner'].sudo().create({
            'name': kwargs.get('name'),
            'phone': kwargs.get('phone'),
            'email': kwargs.get('email'),
        })
        return request.render("vehicle_repair.customer_thanks_form")

    @route('/vehicle/repair/form', methods=['GET'], auth='public', website=True)
    def web_form(self):
        """taking the values of fields from different modules"""
        return request.render('vehicle_repair.web_form_template', {
            'partners': request.env['res.partner'].search([]),
            'users': request.env['res.users'].search([]),
            'vehicle_types': request.env['fleet.vehicle.model.category'].search([]),
            'vehicle_models': request.env['fleet.vehicle.model'].search([])
        })

    @route('/website/form', type='http', auth="public", methods=['POST'], website=True)
    def website_form_vehicle_repair(self, **kwargs):
        """passing the values from form to appropriate fields in Model"""
        request.env['vehicle.repair'].sudo().create({
            'partner_id': kwargs.get('name'),
            'service_advisor_id': kwargs.get('advisor'),
            'vehicle_type_id': kwargs.get('vehicle_type'),
            'vehicle_model_id': kwargs.get('vehicle_model'),
            'vehicle_number': kwargs.get('vehicle_number'),
            'service_type': kwargs.get('service_type'),
        })
        return request.render("vehicle_repair.thanks_form")

    @route('/latest_records', type='json', auth="public", website=True)
    def vehicle_snippet(self):
        """Taking all essential fields from model"""
        vehicle_info = request.env['vehicle.repair'].sudo().search_read([],
                                                                        ['id', 'image', 'partner_id', 'vehicle_type_id',
                                                                         'vehicle_model_id', 'vehicle_number',
                                                                         'service_advisor_id',
                                                                         'reference_no', 'service_type',
                                                                         'customer_complaint',
                                                                         'sum_labour_component_cost'],
                                                                        order='id DESC')
        print("info", vehicle_info)
        records = [vehicle_info[i:i + 4] for i in range(0, len(vehicle_info), 4)]
        return records

    @route(['/snippet_details/<int:data_id>'], type="http", auth="public", website=True)
    def repair_details(self, data_id):
        """taking the data from id passed from form when click image"""
        details = request.env['vehicle.repair'].browse(data_id)
        values = {
            'details': details
        }
        return request.render('vehicle_repair.vehicle_repair_details', values)
