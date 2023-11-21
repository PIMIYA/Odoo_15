import math
from termios import OPOST
from odoo import api, models, fields, exceptions
import logging
from .pycnnum import num2cn
from datetime import datetime
_logger = logging.getLogger(__name__)


class Archived(models.Model):
    _name = 'agriculture.archived'
    _inherit = 'mail.thread'
    _rec_name = 'SellerName'
    _description = 'Archived'
    _order = "LastCreationTime desc"

    # 農民資料
    member = fields.Many2one(
        "res.partner", "Member", required=True)
    SellerName = fields.Char(
        "SellerName", related="member.SellerName")
    SellerId = fields.Char(
        "SellerId", related="member.SellerId")
    Region = fields.Char("Region", related="member.Region")
    FarmerType = fields.Selection(
        "FarmerType", related="member.FarmerType")
    ContractArea = fields.Float(
        "ContractArea", related="member.ContractArea")
    ChishangRArea = fields.Float(
        "ChishangRArea", related="member.ChishangRArea")
    TGAPArea = fields.Float(
        "TGAPArea", related="member.TGAPArea")
    OrganicVerifyDate = fields.Date(
        "OrganicVerifyDate", related="member.OrganicVerifyDate")
    OrganiCertifiedArea = fields.Float(
        "OrganiCertifiedArea", related="member.OrganiCertifiedArea")
    NonLeasedArea = fields.Float(
        "NonLeasedArea", related="member.NonLeasedArea")
    MaxPurchaseQTY = fields.Float(
        "MaxPurchaseQTY", related="member.MaxPurchaseQTY")
    

    # 帳號資料
    MemberBankAccount = fields.Char(
        compute='_compute_MemberBankAccount')
    MemberBankName = fields.Char(compute='_compute_MemberBankName')
    MemberBankAccountHolderName = fields.Char(
        compute='_compute_MemberBankAccountHolderName')

    @api.depends('member')
    def _compute_MemberBankAccount(self):
        for rec in self:
            self.MemberBankAccount = rec.member.get_bank_info()['acc_number']

    @api.depends('member')
    def _compute_MemberBankName(self):
        for rec in self:
            self.MemberBankName = rec.member.get_bank_info()['bank_name']

    @api.depends('member')
    def _compute_MemberBankAccountHolderName(self):
        for rec in self:
            self.MemberBankAccountHolderName = rec.member.get_bank_info()[
                'acc_holder_name']
    ##########

    # 成單的序號列表
    seq_numbers = fields.One2many(
        'agriculture.crop', 'archived_id', 'Numbers of CropRecord', required=True)

    # 額外的資訊
    additional_items = fields.One2many(
        'agriculture.archived_additional_item', 'archived_id', 'Extra Items')
    
    
    #商品購買->應收帳款
    extra_orders = fields.One2many('sale.order', 'archived_id', 'Extra Orders')
    

    # 單據時間
    LastCreationTime = fields.Datetime(
        'LastCreationTime', default=datetime.now())

    # 計算資料
    TotalExpenditure = fields.Float(compute='_compute_TotalExpenditure')
    TotalIncome = fields.Float(compute='_compute_TotalIncome')
    TotalActuallyPaid = fields.Float(compute='_compute_TotalActuallyPaid')
    TotalQTY = fields.Float(compute='_compute_TotalQTY')
    RemianingQTY = fields.Float(compute='_compute_RemianingQTY')
    IsOverflowQTY = fields.Boolean(compute='_compute_IsOverflowQTY')

    @api.depends('seq_numbers')
    def _compute_TotalQTY(self):
        for rec in self:
            rec.TotalQTY = 0
            for crop in rec.seq_numbers:
                rec.TotalQTY += crop.CropWeight

    @api.depends('TotalQTY', 'MaxPurchaseQTY')
    def _compute_RemianingQTY(self):
        for rec in self:
            rec.RemianingQTY = rec.MaxPurchaseQTY - rec.TotalQTY

    @api.onchange('RemianingQTY')
    def _compute_IsOverflowQTY(self):
        for rec in self:
            rec.IsOverflowQTY = rec.RemianingQTY < 0

    @api.depends('seq_numbers', 'additional_items')
    def _compute_TotalExpenditure(self):
        for rec in self:
            rec.TotalExpenditure = 0
            for crop in rec.seq_numbers:
                if crop is not None:
                    rec.TotalExpenditure += crop.TotalPrice
            for item in rec.additional_items:
                if item.item_kind == 'expenditure' and item is not None:
                    rec.TotalExpenditure += item.total_price
            rec.TotalExpenditure = math.floor(rec.TotalExpenditure)

    @api.depends('additional_items', 'extra_orders')
    def _compute_TotalIncome(self):
        for rec in self:
            rec.TotalIncome = 0
            for item in rec.additional_items:
                if item.item_kind == 'income' and item is not None:
                    rec.TotalIncome += item.total_price
            for order in rec.extra_orders:
                if order is not None:
                    rec.TotalIncome += order.amount_total
            rec.TotalIncome = math.floor(rec.TotalIncome)
    
    @api.depends('extra_orders')
    def _compute_extra_order(self):
        extra_order_total_amount = 0
        for rec in self:
            for order in rec.extra_orders:
                extra_order_total_amount += order.amount_total

        return extra_order_total_amount


    @api.depends('TotalExpenditure', 'TotalIncome', 'seq_numbers', 'additional_items')
    def _compute_TotalActuallyPaid(self):
        for rec in self:
            rec.TotalActuallyPaid = math.floor(
                rec.TotalExpenditure - rec.TotalIncome)
    ##########

    @api.onchange('member')
    def _onchange_member(self):
        for seq in self.seq_numbers:
            if seq.SellerName.id != self.member.id:
                raise exceptions.ValidationError(
                    'Sorry, Seller\'s id not matched')

    def get_cn_num(self, input):
        return num2cn(math.floor(input), capitalize=True, traditional=True)

    def get_date(self, input):
        return "{:d}".format(input.year) + "/" + "{:0>2d}".format(input.month) + "/" + "{:0>2d}".format(input.day)

    def unlink(self):
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()

        return super(Archived, self).unlink()


# 修正成單的序號刪除後，對應的成單也要刪除還原狀態

    @api.model
    def delete(self, vals):
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()

    @api.model
    def create(self, vals):
        try:
            _logger.info('Start create method in Archived model')

            # Create the record in the current model
            record = super(Archived, self).create(vals)
            _logger.info('Create archived record!!!!!!!!!!!')

            # Let Odoo compute the TotalActuallyPaid field
            record._compute_TotalActuallyPaid()

            # Access the computed value
            total_actually_paid = record.TotalActuallyPaid
            _logger.info('TotalActuallyPaid: %s', total_actually_paid)

            extra_order_total_amount = record._compute_extra_order()
            _logger.info('Extra_order_total_amount: %s', extra_order_total_amount)

            if total_actually_paid is not None:
                suppler_invoice_amout = total_actually_paid + extra_order_total_amount
                if total_actually_paid > 0 and suppler_invoice_amout != 0:
                    _logger.info('Creating outbound payment')
                    self.env['account.payment'].create({
                        'amount': suppler_invoice_amout,
                        'payment_type': 'outbound',
                        'partner_type': 'supplier',
                        'partner_id': record.member.id,
                        'partner_bank_id': record.member.bank_ids[0].id if record.member.bank_ids else False,
                        # Add other required fields
                    })
                elif total_actually_paid < 0 and suppler_invoice_amout != 0:
                    _logger.info('Creating inbound payment')
                    self.env['account.payment'].create({
                        'amount': suppler_invoice_amout,
                        'payment_type': 'inbound',
                        'partner_type': 'supplier',
                        'partner_id': record.member.id,
                        'partner_bank_id': record.member.bank_ids[0].id if record.member.bank_ids else False,
                        # Add other required fields
                    })

            for order in record.extra_orders:
                order.action_confirm()

            _logger.info('End create method in Archived model')
            return record

        except Exception as e:
            _logger.error('An error occurred: %s', str(e))
            # You can raise the exception again or handle it as needed
            raise


    def write(self, vals):
        try:
            res = super().write(vals)
            # Update the data as needed
            total_actually_paid = self.TotalActuallyPaid
            _logger.info('TotalActuallyPaid: %s', total_actually_paid)

            extra_order_total_amount = self._compute_extra_order()
            _logger.info('Extra_order_total_amount: %s', extra_order_total_amount)

            if total_actually_paid is not None:
                suppler_invoice_amout = total_actually_paid + extra_order_total_amount
                if total_actually_paid > 0 and suppler_invoice_amout != 0:
                    _logger.info('Creating outbound payment')
                    self.env['account.payment'].create({
                        'amount': suppler_invoice_amout,
                        'payment_type': 'outbound',
                        'partner_type': 'supplier',
                        'partner_id': self.member.id,
                        'partner_bank_id': self.member.bank_ids[0].id if self.member.bank_ids else False,
                        # Add other required fields
                    })
                elif total_actually_paid < 0 and suppler_invoice_amout != 0:
                    _logger.info('Creating inbound payment')
                    self.env['account.payment'].create({
                        'amount': suppler_invoice_amout,
                        'payment_type': 'inbound',
                        'partner_type': 'supplier',
                        'partner_id': self.member.id,
                        'partner_bank_id': self.member.bank_ids[0].id if self.member.bank_ids else False,
                        # Add other required fields
                    })

            for order in self.extra_orders:
                order.action_confirm()

            _logger.info('End update method in Archived model')
            return res

        except Exception as e:
            _logger.error('An error occurred: %s', str(e))
            # You can raise the exception again or handle it as needed
            raise
        

