# -*- coding: utf-8 -*-

from odoo import models, fields


class Member(models.Model):
    _name = 'agriculture.member'
    _description = 'Member of agriculture app'

    SellerName = fields.Char()
    SellerId = fields.Char()
    Region = fields.Char()
    AuxId = fields.Char()
