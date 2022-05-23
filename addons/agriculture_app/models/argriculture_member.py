from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Member(models.Model):
    _name = 'agriculture.member'
    _inherit = 'mail.thread'
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

    # @api.model
    # def unlink(self, fields):
    #     _logger.info(f'this is the {fields} going to be deleted')
    #     inherit_res_partner = self.env['res.partner']
    #     _logger.info(f'this is the {inherit_res_partner} going to be deleted')
    #     return super(Member, self).unlink()
