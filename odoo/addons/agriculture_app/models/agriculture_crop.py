# -*- coding: utf-8 -*-

from ast import Store
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)


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
        'organic', '有機耕作')], string='FarmingMethod', required=True)

    CropVariety = fields.Many2one(
        'agriculture.cropvariety', string='CropVariety', required=True)  # 品種 不同品種有不同的加成

    CropVariety_bonus = fields.Integer(
        'CropVariety_bonus', related="CropVariety.CropVariety_bonus", required=True)  # 品種加成bonus

    CropStatus = fields.Selection(
        [('dry', '乾穀'), ('humi', '濕穀')], 'CropStatus', required=True)  # 乾穀 濕穀

    CropType = fields.Selection([('a', '越光米'), (
        'b', '黑糯米'), ('c', '紅糯米')], string='CropType', required=False)  # 特殊米種

    isTAGP = fields.Boolean(
        string="isTAGP", default=False)  # 是否TAGP yes = +100

    FarmingAdaption = fields.Selection(
        [('a', '有機轉型'), ('b', '隔離帶')], string='FarmingAdaption', required=False)  # 農業轉型

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
    archived_id = fields.Many2one("agriculture.archived")

    # new state

    @api.model
    def _default_stage(self):
        Stage = self.env['crop.stage']
        return Stage.search([("state", "=", "draft")], limit=1)

    stage_id = fields.Many2one('crop.stage', default=_default_stage,
                               copy=False, group_expand="_group_expand_stage_id")
    state = fields.Selection(related="stage_id.state")

    def button_refresh(self):
        Stage = self.env['crop.stage']
        draft_stage = Stage.search([("state", "=", "draft")], limit=1)
        # for checkout in self:
        #     checkout.stage_id = done_stage
        return True

    # ******計價資料*****
    # 以計算完成定價
    PriceState = fields.Selection(
        [('draft', '草稿'), ('done', '計價完成'), ('archived', '完成出單')], string='PriceState', default='draft')
    # 底價判斷   底價 / 百台斤
    FinalPrice = fields.Float(
        "FinalPrice", compute="_compute_final_price", store=True)

    # 總價加成
    TotalPrice = fields.Float(
        "TotalPrice", compute="_compute_total_price", store=True)

    @ api.depends('FarmerType',
                  'CropType',
                  'FarmingMethod',
                  'CropVariety_bonus',
                  'VolumeWeight',
                  'PrimeYield',
                  'TasteRating',
                  'BrownIntactRatio',
                  'FarmingAdaption',
                  'isTAGP')
    def _compute_final_price(self):
        for record in self:
            if self._check_nValue(record.VolumeWeight, record.PrimeYield, record.TasteRating, record.BrownIntactRatio):
                if record.FarmerType == 'contract':
                    # 契約農民
                    # 特殊米種
                    if record.CropType == 'a':
                        # 越光米
                        record.FinalPrice = 2600

                    elif record.CropType == 'b' or record.CropType == 'c':
                        # 黑糯米或紅糯米
                        record.FinalPrice = 1700
                    else:
                        # 其他
                        # 有機米
                        if record.FarmingMethod == 'organic':
                            v = True if record.VolumeWeight > 610 else False
                            v2 = True if record.VolumeWeight < 610 and record.VolumeWeight > 560 else False
                            if v is False and v2 is False:
                                record.FinalPrice = 2300
                            elif v is False and v2 is True:
                                record.FinalPrice = 2400
                            elif v is True and record.PrimeYield > 70:
                                record.FinalPrice = 2600
                            elif v is True and record.PrimeYield < 70:
                                record.FinalPrice = 2400
                        else:
                            # 有機轉型或隔離帶
                            if record.FarmingAdaption == 'a' or record.FarmingAdaption == 'b':
                                record.FinalPrice = 2300
                            else:
                                # 慣行耕作
                                compare_list = [self._get_quality_level(record.TasteRating), self._get_quality_level(
                                    record.VolumeWeight), self._get_quality_level(record.BrownIntactRatio)]
                                min_value = min(compare_list)
                                bonus = self._get_compare_price(
                                    min_value, record.PrimeYield) + record.CropVariety_bonus
                                if record.isTAGP:
                                    record.FinalPrice = bonus + 100
                                else:
                                    record.FinalPrice = bonus

                else:
                    # 非契約農民
                    record.FinalPrice = 1400

                record.PriceState = 'done'
            else:
                record.FinalPrice = 0
                record.PriceState = 'draft'

    def _get_quality_level(self, expValue):
        p_list = [609.0, 590.0, 560.0, 540.0]
        x1 = expValue - p_list[3]
        x2 = expValue - p_list[0]
        x3 = expValue - p_list[1]
        x4 = expValue - p_list[2]

        lx1 = 1 if x1 >= 0 else -1
        lx2 = 1 if x2 > 0 else 0
        lx3 = 1 if x3 > 0 else 0
        lx4 = 1 if x4 > 0 else 0

        return lx1 + lx2 + lx3 + lx4

    def _get_compare_price(self, min, PrimeYield):
        # base_price 1550
        if min == 4:
            bonus = 1550 + 180
            return bonus
        elif min == 3:
            bonus = 1550 + 120
            return bonus
        elif min == 2:
            bonus = 1550 + 60
            return bonus
        elif min == 1:
            bonus = 1550
            return bonus
        elif min == -1:
            v = PrimeYield - 63
            bonus = 1550 - v
            return bonus

    def _check_nValue(self, VolumeWeight, PrimeYield, TasteRating, BrownIntactRatio):
        return True if VolumeWeight != 0 or PrimeYield != 0 or TasteRating != 0 or BrownIntactRatio != 0 else False

    @api.depends('CropWeight',
                 'FinalPrice',
                 'FarmerType',
                 'CropType',
                 'FarmingMethod',
                 'CropVariety_bonus',
                 'VolumeWeight',
                 'PrimeYield',
                 'TasteRating',
                 'BrownIntactRatio',
                 'FarmingAdaption',
                 'isTAGP')
    def _compute_total_price(self):
        for record in self:
            unit_tw = record.CropWeight / 60
            record.TotalPrice = unit_tw * record.FinalPrice

    def write(self, vals):
        res = super(Crop, self).write(vals)

        key = 'archived_id'
        if key in vals:
            archivedId = vals[key]
            if archivedId == 0:
                self.PriceState = 'done'
            else:
                self.PriceState = 'archived'

        return res
