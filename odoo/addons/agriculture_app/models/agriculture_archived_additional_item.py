from pkg_resources import require
from odoo import api, models, fields


class ArchivedAdditionalItem(models.Model):
    _name = 'agriculture.archived_additional_item'
    _description = 'Archived Additional Item'
    _rec_name = 'item_name'

    item_name = fields.Char("Item Name", required=True)
    amount = fields.Float("Amount", required=True)
    unit_price = fields.Float("Price Per Unit", required=True)
    total_price = fields.Float(float=0)
    datetime = fields.Datetime('Date', required=True)

    archived_id = fields.Many2one('agriculture.archived')

    @api.onchange('amount', 'unit_price')
    def _onchange_price(self):
        self.total_price = self.amount * self.unit_price
