from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    archived_id = fields.Many2one('agriculture.archived', 'Archived')