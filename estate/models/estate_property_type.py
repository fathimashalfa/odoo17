from odoo import fields, models


class Estate_Property_type(models.Model):
    _name = "estate.property.type"

    name = fields.Char(required=True)
