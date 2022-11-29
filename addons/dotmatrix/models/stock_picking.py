from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class dotmatrix(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    print_data = fields.Text(
        string='Printer Data', readonly=True)

    def action_refresh_printer_data(self):
        temlate = self.env["mail.template"].search(
            [('name', '=', 'Test Template')])
        data = temlate._render_template(
            temlate.body_html, 'stock.picking', self.ids)
        self.print_data = data

    def action_print(self):
        pass

    def button_validate(self):
        res = super(dotmatrix, self).button_validate()
        self.action_refresh_printer_data()
        return res

        # def print_dotmatrix(self):
        #     self.ensure_one()
        #     _logger.info('print_dotmatrix')
        #     return self.env.ref('dotmatrix.action_report_stock_picking').report_action(self)
