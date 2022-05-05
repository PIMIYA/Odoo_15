from termios import OPOST
from odoo import api, models, fields, exceptions
import logging
from .pycnnum import num2cn

_logger = logging.getLogger(__name__)


class Archived(models.Model):
    _name = 'agriculture.archived'
    _description = 'Archived'

    member = fields.Many2one(
        "agriculture.member", "Member", required=True)
    # 成單的序號列表
    seq_numbers = fields.One2many(
        'agriculture.crop', 'archived_id', 'Numbers of CropRecord', required=True)
    # 額外的資訊
    additional_items = fields.One2many(
        'agriculture.archived_additional_item', 'archived_id', 'Extra Items')

    @api.onchange('member')
    def _onchange_member(self):
        for seq in self.seq_numbers:
            if seq.SellerName.id != self.member.id:
                raise exceptions.ValidationError(
                    'Sorry, Seller\'s id not matched')

    def get_cn_num(self, input):
        return num2cn(input, capitalize=True, traditional=True)

    def unlink(self):
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()

        return super(Archived, self).unlink()
