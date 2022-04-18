from odoo import models, fields


class CropVariety(models.Model):
    _name = 'agriculture.cropvariety'
    _description = 'CropVariety of agriculture app'
    _rec_name = 'CropVariety_name'

    CropVariety_name = fields.Char()
    CropVariety_bonus = fields.Integer()
