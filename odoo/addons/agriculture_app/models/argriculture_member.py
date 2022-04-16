# -*- coding: utf-8 -*-

from odoo import models, fields


class Member(models.Model):
    _name = 'agriculture.member'
    _description = 'Member of agriculture app'
    _rec_name = 'SellerName'
    _order = "SellerName desc"

    SellerName = fields.Char()
    SellerId = fields.Char()
    FarmerType = fields.Selection(
        [('non_contract', '非契作農民'), ('contract', '契作農民')], string='FarmerType')
    Region = fields.Char()
    AuxId = fields.Char()
