from email.policy import default
from odoo import models, fields


class Member(models.Model):
    _name = 'agriculture.member'
    _description = 'Member of agriculture app'
    _rec_name = 'SellerName'
    _order = "SellerName desc"

    SellerName = fields.Char(required=False)
    SellerId = fields.Char(required=False)
    FarmerType = fields.Selection(
        [('non_contract', '非契作農民'), ('contract', '契作農民')], string='FarmerType', default='non_contract', required=False)
    Region = fields.Char(required=False)
    AuxId = fields.Char(required=False)

    ContractArea = fields.Float(default=0.0, required=False)
    ChishangRArea = fields.Float(default=0.0, required=False)
    TGAPArea = fields.Float(default=0.0, required=False)

    OrganicVerifyDate = fields.Date(
        'OrganicVerifyDate', required=False)  # 有機認證日期

    OrganiCertifiedArea = fields.Float(default=0.0, required=False)
    NonLeasedArea = fields.Float(default=0.0, required=False)

    '''
        - (If 契作農民 == True) 新增契作面積:
        - 契作面積
        - 池上R面積
        - TGAP面積
        - (If 契作農民 == True) 有機認證日期:
        - 有機認證面積
        - 未契作面積
    '''
