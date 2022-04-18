# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Crop(models.Model):
    _name = "agriculture.crop"
    _description = "Crop"
    _order = "EndTime desc"

    # ******主要使用資料******
    # ******流水號******
    SeqNumber = fields.Char("SeqNumber", required=True)
    # ******農夫的資訊從member中取得******
    SellerName = fields.Many2one(
        "agriculture.member", string="SellerName", required=True)
    SellerId = fields.Char(
        "SellerId", related="SellerName.SellerId", required=True)
    SellerId1 = fields.Char("SellerId1", required=False)
    Region = fields.Char("Region", related="SellerName.Region", required=False)
    AuxId = fields.Char("AuxId", related="SellerName.AuxId", required=False)
    FarmerType = fields.Selection(
        "FarmerType", related="SellerName.FarmerType", required=True)
    # *******************************************
    # ******農作物資料******
    FarmingMethod = fields.Selection([('conventional', '慣行農法'), (
        'organic', '有機耕作'), ('tgap', 'TGAP')], string='FarmingMethod', required=True)

    CropVariety = fields.Many2one(
        'agriculture.cropvariety', string='CropVariety', required=True)  # 品種

    CropStatus = fields.Selection(
        [('dry', '乾穀'), ('humi', '濕穀')], 'CropStatus', required=True)  # 乾穀 濕穀

    CropType = fields.Selection([('a', '越光米'), (
        'b', '黑糯米'), ('c', '紅糯米')], string='CropType', required=False)  # 特殊米種

    BrownYield = fields.Float('BrownYield', required=True)  # 糙米成品率

    HullYield = fields.Float('HullYield', required=True)  # 粗糠成品率

    BranYield = fields.Float('BranYield', required=True)  # 米糠成品率

    PrimeYield = fields.Float('PrimeYield', required=True)  # 白米成品率

    BBRiceYield = fields.Float('BBRiceYield', required=True)  # 大碎米成品率

    SBRiceYield = fields.Float('SBRiceYield', required=True)  # 小碎米成品率

    RawHumidity = fields.Float('RawHumidity', required=True)  # 稻穀濕度

    BrownHumidity = fields.Float('BrownHumidity', required=True)  # 糙米濕度

    RiceHumidity = fields.Float('RiceHumidity', required=True)  # 白米濕度

    BrownIntactRatio = fields.Float(
        'BrownIntactRatio', required=True)  # 糙米-完整粒

    BrownCrackedRatio = fields.Float(
        'BrownCrackedRatio', required=True)  # 糙米-胴裂粒

    BrownImmatureRatio = fields.Float(
        'BrownImmatureRatio', required=True)  # 糙米-未熟粒

    BrownPestsRatio = fields.Float('BrownPestsRatio', required=True)  # 糙米-被害粒

    BrownColoredRatio = fields.Float(
        'BrownColoredRatio', required=True)  # 糙米-染色粒

    BrownDeadRatio = fields.Float('BrownDeadRatio', required=True)  # 糙米-死米

    TasteRating = fields.Float('TasteRating', required=True)  # 食味值

    Protein = fields.Float('Protein', required=True)  # 蛋白質含量

    BrownMoisture = fields.Float('BrownMoisture', required=True)  # 遠紅外線-糙米濕度

    BrownAmylose = fields.Float('BrownAmylose', required=True)  # 直鏈性澱粉含量

    VolumeWeight = fields.Float('VolumeWeight', required=True)  # 容量重量

    CarCropWeight = fields.Float('CarCropWeight', required=True)  # 重車重量

    CarWeight = fields.Float('CarWeight', required=True)  # 車重

    HarvestYear = fields.Integer('HarvestYear', required=True)  # 收穫年份

    HarvestPeriod = fields.Integer('HarvestPeriod', required=True)  # 期數

    LastCreationTime = fields.Datetime(
        'LastCreationTime', required=True)  # 收購時間

    CropWeight = fields.Float('CropWeight', required=True)  # 稻穀總重量

    DryerId = fields.Integer('DryerId', required=True)  # 烘乾機編號

    StorageId = fields.Integer('StorageId', required=True)  # 存放的倉庫編號

    # ******次要資料******

    StartTime = fields.Datetime('Start Time', required=True)
    EndTime = fields.Datetime('End Time', required=True)

    # active = fields.Boolean("Active?", default=True)

    def button_processEstimate(self):
        self.ensure_one()
        print("hello underworld")
        return True

    archived_id = fields.Many2one("agriculture.archived")

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends("value")
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
