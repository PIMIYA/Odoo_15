from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class Invoice_recieve(models.Model):
    _name = 'agriculture.invoice_recieve'
    _description = 'Invoice'
