from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class dotmatrix(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    print_data = fields.Html(
        string='Printer Data', readonly=True)

    def action_refresh_printer_data(self):
        _logger.info(self.carrier_id.name)
        if self.carrier_id:
            if self.carrier_id.name == "宅配通":
                temlate = self.env["mail.template"].search(
                    [('name', '=', '宅配通')])
                data = temlate._render_template(
                    temlate.body_html, 'stock.picking', self.ids)
                self.print_data = data
                _logger.info(data)
            if self.carrier_id.name == "大榮貨運":
                temlate = self.env["mail.template"].search(
                    [('name', '=', '大榮貨運')])
                data = temlate._render_template(
                    temlate.body_html, 'stock.picking', self.ids)
                self.print_data = data
                _logger.info(data)
        else:
            _logger.info('no carrier')
            self.print_data = '請選擇運送方式, 按下更新列印資料，以列印紙本出貨單！'

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
