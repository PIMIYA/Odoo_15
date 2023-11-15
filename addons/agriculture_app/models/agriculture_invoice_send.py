from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class Invoice_send(models.Model):
    _name = 'agriculture.invoice_send'
    _description = 'Invoice'
