from odoo import _, fields, models
import hashlib
import hmac
import logging
import pprint

import requests
from werkzeug.urls import url_join

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_razorpay import const



class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('razorpay2', "Razorpay2")], ondelete={'razorpay2': 'set default'}
    )
    razorpay_key_id = fields.Char(
        string="Razorpay Key Id",
        help="The key solely used to identify the account with Razorpay.",
        required_if_provider='razorpay2',
    )
    razorpay_key_secret = fields.Char(
        string="Razorpay Key Secret",
        required_if_provider='razorpay2',
        groups='base.group_system',
    )
    razorpay_webhook_secret = fields.Char(
        string="Razorpay Webhook Secret",
        required_if_provider='razorpay2',
        groups='base.group_system',
    )

