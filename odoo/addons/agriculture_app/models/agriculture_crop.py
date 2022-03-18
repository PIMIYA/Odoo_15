# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Crop(models.Model):
    _name = "agriculture.crop"
    _description = "Crop"

    name = fields.Char('Crop Name', required=True)

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends("value")
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
