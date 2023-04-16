from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class EcanObt(models.Model):
    _name = 'agriculture.ecan_obt'
    _description = 'e-can OBT'

    StockPickingId = fields.Many2one('stock.picking')
    StockPickingId_Customer = fields.Char(
        "Customer", related="StockPickingId.partner_id.name", required=False)
    OBTNumber = fields.Char('OBTNumber', require=True)
    FileNo = fields.Char('FileNo', require=True)
    ShippingPdf = fields.Binary('ShippingPdf')
    ShippingPdfFilename = fields.Char(
        string='PDF Filename',
        compute='_compute_pdf_filename'
    )

    @api.depends('ShippingPdf')
    def _compute_pdf_filename(self):
        self.ensure_one()
        if not self.FileNo:
            self.ShippingPdfFilename = ''
            return

        self.ShippingPdfFilename = self.FileNo.rsplit('/', 1)[-1]
