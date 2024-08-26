from odoo import models, fields, api


class Inherit_res_company(models.Model):
    _inherit = 'res.company'

    fax = fields.Char(
        string='Fax',
        help="Fax number of the Company",
        required=False
    )
