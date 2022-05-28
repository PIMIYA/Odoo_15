from odoo import models, fields, api, _


class CropStorage(models.Model):
    _name = 'agriculture.storage'
    _inherit = 'mail.thread'
    _description = 'Crop Storage'
    _rec_name = 'StorageId'

    StorageId = fields.Char(string='Storage Id', required=True)

    Crops = fields.One2many(
        'agriculture.crop', 'StorageId', string='Crops')

    CropVarieties = fields.Char('CropVarieties')

    # TotalWeight = fields.Float('Total Weight', default=0.0)
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
