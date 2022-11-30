from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class dotmatrix(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    # print_data = fields.Html(
    #     string='Printer Data', render_engine='qweb', translate=True, sanitize=False)
    print_data = fields.Text(string='Printer Data')

    def action_refresh_printer_data(self):
        _logger.info(self.carrier_id.name)
        if self.carrier_id:
            if self.carrier_id.name == "宅配通":
                template = self.env["mail.template"].search(
                    [('name', '=', '宅配通')])
                data = template._render_template(
                    template.body_html, 'stock.picking', self.ids, engine='qweb')
                '''
                engine = 'inline_template' 'qweb' 'qweb_view'
                https://github.com/odoo/odoo/blob/15.0/addons/mail/models/mail_render_mixin.py
                '''
                temp = data[self.ids[0]]
                # _logger.info(f"temp html: {temp}")
                # _logger.info(f"id : {self.ids[0]}")
                # _logger.info(f"id type: {type(self.ids)}")
                # truncated_text = self.env["ir.fields.converter"].text_from_html(
                #     temp, 40, 100, "...")
                self.print_data = temp
                _logger.info(f"render data : {self.print_data}")

            elif self.carrier_id.name == "大榮貨運":
                template = self.env["mail.template"].search(
                    [('name', '=', '大榮貨運')])
                data = template._render_template(
                    template.body_html, 'stock.picking', self.ids, engine='qweb')
                temp = data[self.ids[0]]
                self.print_data = temp
                _logger.info(f"render data : {self.print_data}")

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
