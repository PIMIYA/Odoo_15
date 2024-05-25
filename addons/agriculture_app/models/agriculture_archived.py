import math
from termios import OPOST
from odoo import api, models, fields, exceptions
import logging
from .pycnnum import num2cn
from .pyzhnum import num2zh
from datetime import datetime
_logger = logging.getLogger(__name__)


class Archived(models.Model):
    _name = 'agriculture.archived'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'SellerName'
    _description = 'Archived'
    _order = "LastCreationTime desc"

    # 農民資料
    member = fields.Many2one(
        "res.partner", "Member", required=True, states={'confirm': [('readonly', True)]})
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
    is_agriculture_member = fields.Boolean(
        "Is an Agriculture Member", related="member.is_agriculture_member")

    state = fields.Selection([
        ('none', 'None'),
        ('draft', 'Draft'),
        ('confirm', 'Confirmed')
    ], default='none')

    def action_none(self):
        self.state = 'none'

    def action_draft(self):
        self.state = 'draft'
        related_payment = self.env['account.payment'].search(
            [('archived_id', '=', self.id)])
        related_payment.action_draft()
        related_payment.action_cancel()
        related_payment.unlink()

        for order in self.extra_orders:
            order.action_cancel()
            order.action_draft()
            order._unlink_except_draft_or_cancel()

    def action_confirm(self):
        self.state = 'confirm'
        # Let Odoo compute the TotalActuallyPaid field
        self._compute_TotalActuallyPaid()
        # Access the computed value
        total_actually_paid = self.TotalActuallyPaid
        _logger.info('TotalActuallyPaid: %s', total_actually_paid)

        self._compute_extra_order()
        # Access the computed value
        extra_order_total_amount = self.TotalExtraOrderAmount
        _logger.info('Extra_order_total_amount: %s', extra_order_total_amount)
        if total_actually_paid is not None:
            suppler_invoice_amount = total_actually_paid + extra_order_total_amount
            if total_actually_paid > 0 and suppler_invoice_amount != 0:
                _logger.info('Creating outbound payment')
                self.env['account.payment'].create({
                    'amount': suppler_invoice_amount,
                    'payment_type': 'outbound',
                    'partner_type': 'supplier',
                    'partner_id': self.member.id,
                    'partner_bank_id': self.member.bank_ids[0].id if self.member.bank_ids else False,
                    'archived_id': self.id,
                    # Add other required fields
                })
            elif total_actually_paid < 0 and suppler_invoice_amount != 0:
                _logger.info('Creating inbound payment')
                self.env['account.payment'].create({
                    'amount': suppler_invoice_amount,
                    'payment_type': 'inbound',
                    'partner_type': 'supplier',
                    'partner_id': self.member.id,
                    'partner_bank_id': self.member.bank_ids[0].id if self.member.bank_ids else False,
                    'archived_id': self.id,
                    # Add other required fields
                })

            for order in self.extra_orders:
                if order.invoice_status is not 'to invoice':
                    order.action_confirm()
                    order._create_invoices()

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
        'agriculture.crop', 'archived_id', 'Numbers of CropRecord', required=True, states={'confirm': [('readonly', True)]})

    # 額外的資訊
    additional_items = fields.One2many(
        'agriculture.archived_additional_item', 'archived_id', 'Extra Items', states={'confirm': [('readonly', True)]})

    # 商品購買->應收帳款
    extra_orders = fields.One2many('sale.order', 'archived_id', 'Extra Orders', states={
                                   'confirm': [('readonly', True)]})

    # account.payment
    suuplier_payment = fields.One2many(
        'account.payment', 'archived_id', 'Supplier Payment')

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
    TotalExtraOrderAmount = fields.Float(compute='_compute_extra_order')

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

    @api.depends('seq_numbers', 'additional_items', 'extra_orders')
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
            rec.TotalExtraOrderAmount = extra_order_total_amount

    @api.depends('TotalExpenditure', 'TotalIncome', 'seq_numbers', 'additional_items', 'extra_orders')
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
        # return num2cn(math.floor(input), alt_two=True, alt_zero=True, capitalize=True, traditional=True)
        digi = math.floor(input)
        return num2zh(digi)

    def get_date(self, input):
        return "{:d}".format(input.year) + "/" + "{:0>2d}".format(input.month) + "/" + "{:0>2d}".format(input.day)

    def unlink(self):
        _logger.info('Start unlink method in Archived model')
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()

        return super(Archived, self).unlink()

    def create_invoices(self):
        extra_orders = self.env['sale.order'].browse(
            self._context.get('archived_id', []))
        for order in extra_orders:
            order._create_invoices()
            for inv in order.invoice_ids:
                # make invoice:
                inv.with_context({'active_model': 'account.move', 'active_ids': inv.ids}).create(
                    {}).action_create_payments()


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
            record._compute_extra_order()
            extra_order_total_amount = record.TotalExtraOrderAmount
            _logger.info('Extra_order_total_amount: %s',
                         extra_order_total_amount)

            # set state to draft
            record.action_draft()

            _logger.info('End create method in Archived model')
            return record

        except Exception as e:
            _logger.error('An error occurred: %s', str(e))
            # You can raise the exception again or handle it as needed
            raise

    def write(self, vals):
        try:
            res = super(Archived, self).write(vals)
            # Update the data as needed
            # total_actually_paid = self.TotalActuallyPaid
            # _logger.info('TotalActuallyPaid: %s', total_actually_paid)

            # extra_order_total_amount = self._compute_extra_order()
            # _logger.info('Extra_order_total_amount: %s', extra_order_total_amount)

            # if total_actually_paid is not None:

            #     suppler_invoice_amount = total_actually_paid + extra_order_total_amount
            #     related_payment = self.env['account.payment'].search([('archived_id', '=', self.suuplier_payment.archived_id.id)])

            #     if total_actually_paid > 0 and suppler_invoice_amount != 0:
            #         _logger.info('updating outbound payment')
            #         # Update the related account.payment records
            #         related_payment.action_draft()
            #         related_payment.write({
            #             'amount': suppler_invoice_amount,
            #             'payment_type': 'outbound',
            #         })
            #     elif total_actually_paid < 0 and suppler_invoice_amount != 0:
            #         _logger.info('updating inbound payment')
            #         related_payment.action_draft()
            #         related_payment.write({
            #             'amount': suppler_invoice_amount,
            #             'payment_type': 'inbound',
            #         })

            # for order in self.extra_orders:
            #     if order.invoice_status is 'to invoice':
            #         order._create_invoices()

            _logger.info('End update method in Archived model')
            return res

        except Exception as e:
            _logger.error('An error occurred: %s', str(e))
            # You can raise the exception again or handle it as needed
            raise
