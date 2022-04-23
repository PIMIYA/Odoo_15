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
        'agriculture.crop', 'archived_id', 'Seq Numbers', required=True)
    # 額外的資訊
    additional_items = fields.One2many(
        'agriculture.archived_additional_item', 'archived_id', 'Items')

    @api.onchange('member')
    def _onchange_member(self):
        for seq in self.seq_numbers:
            if seq.SellerName.id != self.member.id:
                raise exceptions.ValidationError(
                    'Sorry, Seller\'s id not matched')

    def get_cn_num(self, input):
        return num2cn(input, capitalize=True, traditional=True)

    # def _process_write_seq_numbers(self, commands):
    #     modelName = 'agriculture.crop'
    #     target = self.env[modelName]
    #     for cmd in commands:
    #         cVal, param1, param2 = cmd
    #         if cVal == 0:  # create
    #             pass
    #         elif cVal == 1:  # update
    #             pass
    #         elif cVal == 2:  # delete
    #             pass
    #         elif cVal == 3:  # unlink
    #             o = target.browse(param1)
    #             o.PriceState = 'done'
    #         elif cVal == 4:  # link
    #             o = target.browse(param1)
    #             o.PriceState = 'archived'
    #         elif cVal == 5:  # clear
    #             pass
    #         elif cVal == 6:  # set
    #             for id in param2:
    #                 o = target.browse(id)
    #                 o.PriceState = 'archived'

    # def _process_write_additional_items(self, commands):
    #     modelName = 'agriculture.archived_additional_item'
    #     target = self.env[modelName]
    #     for cmd in commands:
    #         cVal, param1, param2 = cmd
    #         if cVal == 0:  # create
    #             pass
    #         elif cVal == 1:  # update
    #             pass
    #         elif cVal == 2:  # delete
    #             pass
    #         elif cVal == 3:  # unlink
    #             o = target.browse(param1)
    #         elif cVal == 4:  # link
    #             pass
    #         elif cVal == 5:  # clear
    #             pass
    #         elif cVal == 6:  # set
    #             for id in param2:
    #                 o = target.browse(id)

    # def write(self, vals: dict):
    #     res = super(Archived, self).write(vals)
    #     fileds = [('seq_numbers', self._process_write_seq_numbers),
    #               ('additional_items', self._process_write_additional_items)]
    #     for field in fileds:
    #         key, func = field
    #         if key in vals:
    #             commands = vals[key]
    #             func(commands)
    #     return res
