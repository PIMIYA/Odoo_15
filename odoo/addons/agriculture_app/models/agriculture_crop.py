# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Crop(models.Model):
    _name = "agriculture.crop"
    _description = "Crop"

    # ******主要使用資料******
    SeqNumber = fields.Char("SeqNumber", required=True)
    SellerId = fields.Char("SellerId", required=True)
    SellerId1 = fields.Char("SellerId1", required=False)
    SellerName = fields.Many2one(
        "agriculture.member", "SellerName", required=True)
    Region = fields.Char("Region", required=True)
    AuxId = fields.Char("AuxId", required=True)
    # 農夫的資訊從member中取得
    FarmerType = fields.Selection(
        [('non_contract', '非契作農民'), ('contract', '契作農民')], string='FarmerType', required=True)
    FarmingMethod = fields.Selection([('conventional', '慣行農法'), (
        'organic', '有機耕作'), ('tgap', 'TGAP')], string='FarmingMethod', required=True)
    CropVariety = fields.Char('CropVariety', required=True)
    # 米的品種是否需要與crop_variety一起關聯設定
    CropType = fields.Selection([('a', '越光米'), (
        'b', '黑糯米'), ('c', '紅糯米')], string='CropType', required=False)
    first_estimated_price = fields.Integer(
        'First Estimated Price', required=True)
    total_weight_vehicle = fields.Integer(
        'Total Weight Vehicle', required=True)
    # 全重車輛的載重量
    unload_weight_vehicle = fields.Integer(
        'Unload Weight Vehicle', required=True)
    # 卸載重車輛的載重量
    CropWeight = fields.Integer('CropWeight', required=True)
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

    # ******次要資料******

    StartTime = fields.Datetime('Start Time', required=True)
    EndTime = fields.Datetime('End Time', required=True)

    active = fields.Boolean("Active?", default=True)

    archived_id = fields.Many2one("agriculture.archived")

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends("value")
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
