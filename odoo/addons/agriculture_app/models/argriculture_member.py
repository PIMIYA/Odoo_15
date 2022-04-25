from odoo import models, fields


class Member(models.Model):
    _name = 'agriculture.member'
    _description = 'Member of agriculture app'
    _rec_name = 'SellerName'
    _order = "SellerName desc"

    SellerName = fields.Char()
    SellerId = fields.Char()
    FarmerType = fields.Selection(
        [('non_contract', '非契作農民'), ('contract', '契作農民')], string='FarmerType', default='non_contract')
    Region = fields.Char()
    AuxId = fields.Char()

    OrganicVerifyDate = fields.Date(
        'OrganicVerifyDate', required=False)  # 有機認證日期

    '''
        - (If 契作農民 == True) 新增契作面積:
        - 契作面積
        - 池上R面積
        - TGAP面積
        - (If 契作農民 == True) 有機認證日期
    '''
