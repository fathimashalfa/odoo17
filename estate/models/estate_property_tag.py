from odoo import fields, models


class Estate_Property_tag(models.Model):
    _name = "estate.property.tag"

    name = fields.Char(required=True, string="Name")
