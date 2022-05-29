from odoo import api, models, fields
import logging


_logger = logging.getLogger(__name__)


class Storage(models.Model):
    _name = 'agriculture.storage'
    _description = 'Storage of agriculture app'
    _rec_name = 'StorageId'

    # 存放的倉庫編號 # this work 2
    StorageId = fields.Char(string='Storage Id', required=True)

    # 有StorageId的Crop # this work 2
    Crops = fields.One2many(
        'agriculture.crop', 'StorageId', string='Crops')

    CropVarieties = fields.Char('CropVarieties')

    TotalWeight = fields.Float(
        'Total Weight', compute='_onchange_Crops', store=True)

    @api.depends('Crops')
    def _onchange_Crops(self):
        cvWeight = []
        cv = []
        for rec in self:
            if rec.Crops:
                for w in rec.Crops:
                    cvWeight.append(w.CropWeight)
                    for c in w.CropVariety:
                        cv.append(c.CropVariety_name)
        rec.TotalWeight = sum(cvWeight)
        rec.CropVarieties = cv
