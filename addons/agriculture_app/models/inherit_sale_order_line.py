from odoo import models, fields, api


class inherit_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    barcode = fields.Char('Barcode', related='product_id.barcode')
