from odoo import models, fields


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
