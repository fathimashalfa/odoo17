# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class VehicleRepair(models.Model):
    _name = "vehicle.repair"
    _description = "Vehicle Repair"
    _inherit = 'mail.thread'
    _rec_name = "reference_no"

    reference_no = fields.Char(string='Reference No', copy=False, index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one(string="Customer", comodel_name='res.partner', required=True)
    service_advisor_id = fields.Many2one(string='Service Advisor', comodel_name='res.users',
                                         default=lambda self: self.env.user)
    vehicle_type_id = fields.Many2one(string="Vehicle type", comodel_name='fleet.vehicle.model.category',
                                      ondelete='set null')
    vehicle_model_id = fields.Many2one(string="Vehicle Model", comodel_name='fleet.vehicle.model')
    vehicle_number = fields.Char(string="Vehicle Number", copy=False, required=True)
    image = fields.Image()
    mobile = fields.Char(string="Mobile", related='partner_id.phone', readonly=False)
    active = fields.Boolean(string="Active", default=True)
    start_date = fields.Date(string="Start Date", default=fields.Date.today())
    duration = fields.Float(string="Duration")
    delivery_date = fields.Date(string="Delivery date")
    service_type = fields.Selection([
        ('free', 'Free'),
        ('paid', 'Paid'), ], default="free", required=True)
    estimated_amount = fields.Float(string="Estimated Amount")
    currency_id = fields.Many2one(string="Currency", comodel_name="res.currency",
                                  default=lambda self: self.env.company.currency_id.id)
    customer_complaint = fields.Html(string="Customer Complaint")
    tag_ids = fields.Many2many(string="Tags", comodel_name='repair.tag')
    state = fields.Selection([('draft', 'Draft'),
                              ('in-progress', 'In-progress'),
                              ('ready_for_delivery', 'Ready for Delivery'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], default="draft", help="mention the state", tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company, readonly="True")
    labour_line_ids = fields.One2many('labour.cost.line', 'labour_id', string="Labour cost")

    total = fields.Monetary(compute="_compute_total", string='Total')
    totals = fields.Monetary(compute="_compute_totals")
    sum_labour_component_cost = fields.Monetary(compute="_compute_sum", string="sum of labor and parts:", store=True)
    consumed_line_ids = fields.One2many(string='Consumed Parts', comodel_name='consumable.parts.line',
                                        inverse_name='parts_id')
    estimated_delivery_date = fields.Date(string="Estimated Delivery Date")
    repair_invoice_id = fields.Many2one(comodel_name='account.move')
    payment_ribbon = fields.Char(compute='_compute_badge')
    invoice_count = fields.Integer(compute="_compute_invoice_count")
    is_invoice = fields.Boolean()
    tomorrow_date = fields.Date(default=fields.Date.today() + relativedelta(days=1))
    date_last_stage_update = fields.Datetime(
        'Last Stage Update', compute='_compute_date_last_stage_update', readonly=False, store=True)

    @api.depends('state')
    def _compute_date_last_stage_update(self):
        for rec in self:
            rec.date_last_stage_update = self.env.cr.now()

    def action_archive(self):
        records = self.env['vehicle.repair'].search([('state', '=', 'canceled')])
        print(records, "hello")
        records.active = False
        print("hello guys")
        return super().action_archive()

    @api.depends('repair_invoice_id')
    def _compute_badge(self):
        for record in self:
            record.payment_ribbon = record.repair_invoice_id.payment_state

    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.repair_invoice_id)

    @api.constrains('vehicle_number')
    def _check_vehicle_number(self):
        for rec in self:
            domain = [('vehicle_number', '=', rec.vehicle_number),
                      ('start_date', '=', fields.Date.today())]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError(_("The vehicle  No should be unique"))

    def action_view_invoice(self):
        print(self.repair_invoice_id)
        return {
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'context': {'default_move_type': 'out_invoice'},
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.repair_invoice_id.id
        }

    @api.depends("total", "totals")
    def _compute_sum(self):
        for record in self:
            record.sum_labour_component_cost = record.total + record.totals

    @api.depends('labour_line_ids.subtotal_amount')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.labour_line_ids.mapped('subtotal_amount'))

    @api.depends('consumed_line_ids.subtotal')
    def _compute_totals(self):
        for record in self:
            record.totals = sum(record.consumed_line_ids.mapped('subtotal'))

    @api.model
    def create(self, vals_list):
        if vals_list.get('reference_no', 'New') == 'New':
            vals_list['reference_no'] = self.env['ir.sequence'].next_by_code('vehicle.sequence') or 'New'
        return super(VehicleRepair, self).create(vals_list)

    def create_invoice(self):
        invoice = self.env['account.move'].search(
            [('state', '=', 'draft'), ('partner_id', '=', self.partner_id.id),
             ('move_type', '=', 'out_invoice')], limit=1)
        print(invoice)
        if invoice:
            for rec in self.labour_line_ids:
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': self.env.ref('vehicle_repair.product_vehicle').id,
                        'name': line.employee_id.name,
                        'quantity': line.hours_spent,
                        'price_unit': line.hourly_costs,
                    }) for line in rec]
                })
            for record in self.consumed_line_ids:
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': line.consumed_product_id.id,
                        'name': line.consumed_product_id.name,
                        'quantity': line.quantity,
                        'price_unit': line.unit_price,
                    }) for line in record]
                })
        else:

            invoice = self.env['account.move'].create([
                {
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.context_today(self),
                    'partner_id': self.partner_id.id,
                    'currency_id': self.currency_id.id,
                }])
            for rec in self.labour_line_ids:
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': self.env.ref('vehicle_repair.product_vehicle').id,
                        'name': line.employee_id.name,
                        'quantity': line.hours_spent,
                        'price_unit': line.hourly_costs,
                    }) for line in rec]
                })
            for record in self.consumed_line_ids:
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': line.consumed_product_id.id,
                        'name': line.consumed_product_id.name,
                        'quantity': line.quantity,
                        'price_unit': line.unit_price,
                    }) for line in record]
                })
                print(invoice.id, "hello")
        self.repair_invoice_id = invoice.id
        self.is_invoice = True
        return {
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'context': {'default_move_type': 'out_invoice'},
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': invoice.id

        }

    def confirm(self):
        self.state = "in-progress"

    def done(self):
        self.state = "done"

    def cancel(self):
        self.state = "canceled"

    def ready_for_delivery(self):
        self.delivery_date = fields.Date.today()
        mail_template = self.env.ref('vehicle_repair.email_template_data')
        mail_template.send_mail(self.id, force_send=True)
        self.state = "ready_for_delivery"

    def archive_records(self):
        before_one_month = datetime.now() - timedelta(days=30)
        cancelled_records = self.env['vehicle.repair'].search(
            [('state', '=', 'canceled'), ('date_last_stage_update', '>=', before_one_month)])
        for records in cancelled_records:
            records.active = False

    @api.model
    def change_state(self):
        self.partner_id.write({
            'state': 'service_customer'
        })


class LabourCostLine(models.Model):
    _name = "labour.cost.line"
    _description = "LabourCostLines"

    labour_details = fields.Char(string="Labour Details")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    labour_id = fields.Many2one('vehicle.repair', string="Labour cost id")
    hours_spent = fields.Float(string="Hours Spent")
    hourly_costs = fields.Monetary(string="Hourly Cost", related="employee_id.hourly_cost")
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  default=lambda self: self.env.company.currency_id.id)
    subtotal_amount = fields.Monetary(string="SubTotal", compute="_compute_subtotal", )

    @api.depends("hours_spent", "hourly_costs")
    def _compute_subtotal(self):
        for record in self:
            record.subtotal_amount = record.hours_spent * record.hourly_costs


class ConsumablePartsLine(models.Model):
    _name = "consumable.parts.line"
    _description = "Consumable Parts Line"

    consumed_product_id = fields.Many2one(string='Consumed Products', comodel_name="product.product")
    quantity = fields.Integer(string="Quantity", default=1)
    unit_price = fields.Float(string="Unit Price", related="consumed_product_id.lst_price")
    subtotal = fields.Monetary(string="SubTotal", compute="_compute_subtotal")
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  default=lambda self: self.env.company.currency_id.id)
    parts_id = fields.Many2one(string="consumed part id", comodel_name="vehicle.repair", )

    @api.depends("quantity", "unit_price")
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.unit_price
