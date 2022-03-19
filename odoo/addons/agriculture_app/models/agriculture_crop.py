# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Crop(models.Model):
    _name = "agriculture.crop"
    _description = "Crop"

    order_number = fields.Char("Order Number", required=True)
    famer_number = fields.Char("Famer Number", required=True)
    farmer_info = fields.Many2one(
        'res.partner', string='Farmer Info', required=True)
    # 農夫的資訊從res.partner中取得，資料表名稱為res.partner，以下的農夫類型再以tag填入res.partner中
    farmer_type = fields.Selection(
        [('non_contract', '非契作農民'), ('contract', '契作農民')], string='Farmer Type', required=True)
    crop_type = fields.Selection([('conventional', '慣行農法'), (
        'organic', '有機耕作'), ('tgap', 'TGAP')], string='Crop Type', required=True)
    crop_variety = fields.Char('Crop Variety', required=True)
    # 米的品種是否需要與crop_variety一起關聯設定
    crop_type = fields.Char('Crop Type', required=True)
    first_estimated_price = fields.Integer(
        'First Estimated Price', required=True)
    total_weight_vehicle = fields.Integer(
        'Total Weight Vehicle', required=True)
    # 全重車輛的載重量
    unload_weight_vehicle = fields.Integer(
        'Unload Weight Vehicle', required=True)
    # 卸載重車輛的載重量
    total_crop_weight = fields.Integer('Total Crop Weight', required=True)
    # 米的重量
    crop_humility = fields.Integer('Crop Humility', required=True)

    # 米的濕度 （0-100 ％) 乾穀 <= 15% 濕穀 > 15% 計算後顯示
    crop_humility_type = fields.Selection(
        [('dry', '乾穀'), ('humi', '濕穀')], 'Crop Humility Type', required=True)
    dry_crop_cubic_weight = fields.Integer(
        'Dry Crop Cubic Weight', required=True)
    # 米的立方重量
    crop_conversion_rate = fields.Integer(
        'Crop Conversion Rate', required=True)
    # 米的轉換率 (0-100 ％)
    dry_crop_weight = fields.Integer('Dry Crop Weight', required=True)

    active = fields.Boolean("Active?", default=True)

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends("value")
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
