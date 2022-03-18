# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Crop(models.Model):
    _name = "agriculture.crop"
    _description = "Crop"

    crop_name = fields.Char('Crop Name', required=True)
    crop_type = fields.Char('Crop Type', required=True)
    crop_variety = fields.Char('Crop Variety', required=True)
    farmer = fields.Many2one('res.partner', string='Farmer', required=True)
    farmer_id = fields.Char('Farmer ID', required=True)
    farmer_name = fields.Char('Farmer Name', required=True)
    farmer_phone = fields.Char('Farmer Phone', required=True)
    farmer_email = fields.Char('Farmer Email', required=True)
    farmer_address = fields.Char('Farmer Address', required=True)
    farmer_city = fields.Char('Farmer City', required=True)
    farmer_state = fields.Char('Farmer State', required=True)
    farmer_type = fields.Selection(
        [('non_contract', '非契作農民'), ('contract', '契作農民')], string='Farmer Type', required=True)
    active = fields.Boolean("Active?", default=True)

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends("value")
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
