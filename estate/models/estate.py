from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Estate(models.Model):
    _name = "estate"
    _description = "This is a Real Estate app"

    name = fields.Char(string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
    ], required=True, default='South')
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')])
    available_from = fields.Date(copy=False, default=fields.Date.today()+relativedelta(months=3))
    property_type_id = fields.Integer()
    buyer = fields.Char(copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    product_type = fields.Many2one("estate.property.type", string="Product Type")
