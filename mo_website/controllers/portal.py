# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request


class PortalController(http.Controller):

    @http.route('/my/manufacture', type='http', auth="user", website=True)
    def portal_my_manufacture(self, **kwargs):
        c_user = request.env.user.id
        orders = request.env['mrp.production'].sudo().search([('user_id', '=', c_user)])
        return request.render('mo_website.portal_my_manufacture',
                              {'orders': orders, 'page_name': 'Manufacture'})
