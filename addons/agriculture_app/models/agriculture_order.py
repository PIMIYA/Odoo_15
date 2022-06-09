from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class Crop(models.Model):
    _name = 'agriculture.order'
    _description = 'Agriculture Order'

    category = fields.Selection(
        [('b2b', 'B2B'), ('b2c', 'B2C')], string='Category')

    customer = fields.Many2one('res.partner', string='Customer')

    order_date = fields.Date(string='Order Date')

    order_no = fields.Char(string='Order No')

    quantity = fields.Integer(string='Quantity')

    # unit = fields.Many2one('product.uom', string='Unit')

    weight = fields.Float(string='Weight')

    total_weight = fields.Float(string='Total Weight')

    product = fields.Many2one('product.template', string='Product')
    # price = fields.Monetary(string='Price', related='product.list_price')

    total_price = fields.Float(string='Total Price')

    order_status = fields.Selection([('pending', 'Pending'), (
        'in_progress', 'In Progress'), ('completed', 'Completed')], string='Order Status')
