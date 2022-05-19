import math
from termios import OPOST
from odoo import api, models, fields, exceptions
import logging
from .pycnnum import num2cn

_logger = logging.getLogger(__name__)


class Archived(models.Model):
    _name = 'agriculture.archived'
    _description = 'Archived'

    # 農民資料
    member = fields.Many2one(
        "agriculture.member", "Member", required=True)
    SellerName = fields.Char(
        "SellerName", related="member.SellerName", required=True)
    SellerId = fields.Char(
        "SellerId", related="member.SellerId", required=True)
    Region = fields.Char("Region", related="member.Region", required=True)
    FarmerType = fields.Selection(
        "FarmerType", related="member.FarmerType", required=True)
    ContractArea = fields.Float(
        "ContractArea", related="member.ContractArea", required=True)
    ChishangRArea = fields.Float(
        "ChishangRArea", related="member.ChishangRArea", required=True)
    TGAPArea = fields.Float(
        "TGAPArea", related="member.TGAPArea", required=True)
    OrganicVerifyDate = fields.Date(
        "OrganicVerifyDate", related="member.OrganicVerifyDate", required=True)
    OrganiCertifiedArea = fields.Float(
        "OrganiCertifiedArea", related="member.OrganiCertifiedArea", required=True)
    NonLeasedArea = fields.Float(
        "NonLeasedArea", related="member.NonLeasedArea", required=True)
    ##########

    # 成單的序號列表
    seq_numbers = fields.One2many(
        'agriculture.crop', 'archived_id', 'Numbers of CropRecord', required=True)
    ##########

    # 額外的資訊
    additional_items = fields.One2many(
        'agriculture.archived_additional_item', 'archived_id', 'Extra Items')
    ##########

    @api.onchange('member')
    def _onchange_member(self):
        for seq in self.seq_numbers:
            if seq.SellerName.id != self.member.id:
                raise exceptions.ValidationError(
                    'Sorry, Seller\'s id not matched')

    def get_cn_num(self, input):
        return num2cn(math.floor(input), capitalize=True, traditional=True)

    def unlink(self):
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()

        return super(Archived, self).unlink()
