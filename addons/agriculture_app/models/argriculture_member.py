from odoo import models, fields, api, _
from types import SimpleNamespace
import logging

_logger = logging.getLogger(__name__)


class Member(models.Model):
    # _name = 'agriculture.member'
    _inherit = ['res.partner']
    # _description = 'Member of agriculture app'
    # _rec_name = 'SellerName'
    # _order = "SellerName desc"

    is_agriculture_member = fields.Boolean(string='Is an Agriculture Member', default=False,
                                           help="Check if the contact is a agriculture_member, otherwise it is a person or company", required=False)

    # channel_ids = fields.Many2many('partner_id', 'channel_id', copy=False)

    SellerName = fields.Char(related='name', required=False)
    SellerId = fields.Char(string='SellerId', required=True,
                           readonly=True, default=lambda self: _('New'))
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

    MaxPurchaseQTY = fields.Float(compute='_compute_QTY')

    @api.depends('ContractArea')
    def _compute_QTY(self):
        params = self.env['ir.config_parameter'].sudo()
        maxPurchaseQTYPerHectare = float(params.get_param(
            'agriculture.maxPurchaseQTYPerHectare'))
        for rec in self:
            rec.MaxPurchaseQTY = rec.ContractArea * maxPurchaseQTYPerHectare

    def get_partner_attr(self, attr):
        for rec in self:
            _partner = self.env['res.partner']
            partnerData = _partner.search(
                [("SellerId", "=", rec.SellerId)], limit=1)
            if partnerData:
                if attr == 'address':
                    return "{zip}{country}{city}{state}{street}{street2}".format(
                        zip=partnerData['zip'] if partnerData['zip'] else '',
                        country='({0}) '.format(
                            partnerData['country_id'].name) if partnerData['country_id'].name else '',
                        city=partnerData['city'] if partnerData['city'] else '',
                        state=partnerData['state_id'].name if partnerData['state_id'].name else '',
                        street=partnerData['street'] if partnerData['street'] else '',
                        street2=partnerData['street2'] if partnerData['street2'] else '')
                elif attr == 'total-phone':
                    phones = []
                    if partnerData['phone']:
                        phones.append(partnerData['phone'])
                    if partnerData['mobile']:
                        phones.append(partnerData['mobile'])
                    return ', '.join(str(x) for x in phones)
                elif attr == 'phone-or-mobile':
                    if partnerData['phone']:
                        return partnerData['phone']
                    if partnerData['mobile']:
                        return partnerData['mobile']
                    return ""
                elif attr == 'mobile-or-phone':
                    if partnerData['mobile']:
                        return partnerData['mobile']
                    if partnerData['phone']:
                        return partnerData['phone']
                    return ""
                else:
                    return partnerData[attr]

    def get_bank_info(self):
        result = {}
        result['acc_number'] = ""
        result['bank_name'] = ""
        result['acc_holder_name'] = ""

        for rec in self:
            _partner = self.env['res.partner']
            partnerData = _partner.search(
                [("SellerId", "=", rec.SellerId)], limit=1)
            if not partnerData:
                return result
            if not partnerData['bank_ids']:
                return result
            if not partnerData['bank_ids'][0]:
                return result
            result['acc_number'] = partnerData['bank_ids'][0].acc_number
            result['bank_name'] = partnerData['bank_ids'][0].bank_name
            result['acc_holder_name'] = partnerData['bank_ids'][0].acc_holder_name
        return result

    @api.model
    def create(self, fields):
        _logger.info('Start create method in Member model')
        # add new check type is_agriculture_member
        if fields.get("is_agriculture_member") == True:
            try:
                if fields.get('SellerId', _('New')) == _('New'):
                    fields['SellerId'] = self.env['ir.sequence'].next_by_code(
                        'new.sellerID') or _('New')
                    _logger.info('SellerId: %s', fields['SellerId'])
            except Exception as e:
                _logger.error('Error generating sequence: %s', str(e))
        else:
            fields['is_agriculture_member'] = False

        res = super(Member, self).create(fields)
        return res

    def write(self, fields):
        _logger.info('Start write method in Member model')
        if fields.get('is_agriculture_member') == True and fields.get('SellerId') == _('New'):
            try:
                if fields.get('SellerId', _('New')) == _('New'):
                    fields['SellerId'] = self.env['ir.sequence'].next_by_code(
                        'new.sellerID') or _('New')
                    _logger.info('SellerId: %s', fields['SellerId'])
            except Exception as e:
                _logger.error('Error generating sequence: %s', str(e))
        else:
            pass

        res = super(Member, self).write(fields)
        return res
