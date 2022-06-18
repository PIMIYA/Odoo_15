from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class BlackcatObt(models.Model):
    _name = 'agriculture.blackcat_obt'
    _description = 'Blackcat OBT'

    StockPickingId = fields.Many2one('stock.picking')
    SrvTranId = fields.Char('SrvTranId', require=True)
    OBTNumber = fields.Char('OBTNumber', require=True)
    FileNo = fields.Char('FileNo', require=True)
