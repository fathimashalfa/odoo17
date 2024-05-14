# -*- coding: utf-8 -*-
from odoo import models, fields



class ResPartner(models.Model):
    _inherit = 'res.partner'

    def create_xml(self):
        template = self.env.ref('xmlapi.test_template')
        xml_content = self.env["ir.ui.view"]._render_template(template.id, {'partner': self})
        self.env['ir.attachment'].create({
            'name': f'{self.name} XML File.xml',
            'raw': xml_content.encode(),
            'res_model': self._name,
            'res_id': self.id,
            'minetype': 'application/xml'
        })
