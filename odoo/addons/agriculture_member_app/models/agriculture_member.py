# -*- coding: utf-8 -*-

from odoo import models, fields


class AgricultureMember(models.Model):
    _name = 'agriculture_app.member'
    _description = 'Member of agriculture app'

    SellerName = fields.Char()
    SellerId = fields.Char()
    Region = fields.Char()
    AuxId = fields.Char()
