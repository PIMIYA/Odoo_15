from pkg_resources import require
from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class BlackcatObt(models.Model):
    _name = 'agriculture.blackcat_obt'
    _description = 'Blackcat OBT'

    orderPicking = fields.One2many(
        'stock.picking', 'blackcat_obt_id', 'Picking', required=True)
    SrvTranId = fields.Char('SrvTranId', require=True)
    OBTNumber = fields.Char('OBTNumber', require=True)
    FileNo = fields.Char('FileNo', require=True)
