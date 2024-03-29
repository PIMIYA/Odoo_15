from odoo import models, fields, api, tools, _, exceptions
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class dotmatrix(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    print_data = fields.Html(string='Print Data')

    sender_name = fields.Char(string='Sender Name')
    sender_phone = fields.Char(string='Sender Phone')
    sender_address = fields.Char(string='Sender Address')
    sender_mobile = fields.Char(string='Sender Mobile')
    sender_zip = fields.Char(string='Sender Zip')
    ecan_customerId = fields.Char(string='ECAN Customer ID')
    ktj_customerId = fields.Char(string='KTJ Customer ID')

    def action_refresh_printer_data(self):
        current_company = self.env.company
        if not current_company.phone:
            raise exceptions.ValidationError(
                'Company phone must not be empty')
        if current_company.state_id.name == current_company.city:
            senderAddress = "{0}{1}".format(
                current_company.city, current_company.street)
        else:
            senderAddress = "{0}{1}{2}".format(
                current_company.state_id.name, current_company.city, current_company.street)

        if not senderAddress:
            raise exceptions.ValidationError(
                'Company address must not be empty')

        self.sender_name = current_company.name
        self.sender_address = senderAddress
        self.sender_phone = current_company.phone
        self.sender_mobile = current_company.mobile
        self.sender_zip = current_company.zip

        config = self.env['ir.config_parameter'].sudo()
        self.ecan_customerId = config.get_param('agriculture.ecan_customer_id')
        self.ktj_customerId = config.get_param('agriculture.ktj_customer_id')

        _logger.info(f"sender_name: {self.sender_name}",
                     f"sender_zip: {self.sender_zip}",
                     f"sender_address: {self.sender_address}",
                     f"sender_phone: {self.sender_phone}",
                     f"sender_mobile: {self.sender_mobile}",
                     )

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
                raise exceptions.ValidationError(
                    '請選擇運送方式, 按下更新列印資料，以列印紙本出貨單！或是選擇電子出單！')
        else:
            _logger.info('no carrier')
            raise exceptions.ValidationError(
                '請選擇運送方式, 按下更新列印資料，以列印紙本出貨單！或是選擇電子出單！')

    @api.onchange('carrier_id')
    def onchange_carrier_id(self):
        if self.carrier_id.name == "宅配通" or self.carrier_id.name == "大榮貨運":
            self.action_refresh_printer_data()
        else:
            pass

    def logistic_print(self):
        _logger.info('logistic_print')
        self.action_refresh_printer_data()
        if self.carrier_id.name == "宅配通" or self.carrier_id.name == "大榮貨運":
            return self.env.ref('dotmatrix.action_logistic_report').report_action(self)
        else:
            pass
