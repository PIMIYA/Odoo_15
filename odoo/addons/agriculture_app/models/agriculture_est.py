from odoo import fields, models


class Estimate(models.Model):
    _name = 'agriculture.estimate'
    _description = 'Estimate'

    # ******主要使用資料******
    SeqNumber = fields.Char("SeqNumber", required=True)
