from odoo import models, fields, api, _


class Preferences(models.TransientModel):
    _inherit = 'res.config.settings'

    # Fields
    # ----------------------------------------------------------
    # General
    VolumeWeight_Over_560_price = fields.Integer(
        'Volume Weight Over 560 Price', default=1400, required=True)
