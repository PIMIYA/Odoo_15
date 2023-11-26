from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    archived_id = fields.Many2one('agriculture.archived', 'Archived')