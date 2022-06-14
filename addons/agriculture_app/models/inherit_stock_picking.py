from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    def doBlackCat(self, packageItems):
        for item in packageItems:
            _logger.info(item.product_id)
        '''
        customer
            name
            phone
            address
        sender(company info)
            name
            phone
            address
        product name
        shipment data > 寄送日
        delivery date > 希望到達日 (需要新增)
        '''
        _logger.info('customer.name: {0}'.format(self.partner_id.SellerName))
        _logger.info('customer.phone: {0}'.format(
            self.partner_id.Member.get_partner_attr('total-phone')))
        _logger.info('customer.address: {0}'.format(
            self.partner_id.Member.get_partner_attr('address')))
        _logger.info('==========')
        current_company = self.env.company
        _logger.info('customer.name: {0}'.format(current_company.name))
        _logger.info('customer.phone: {0}'.format(current_company.phone))
        _logger.info('customer.address: {0}{1}'.format(
            current_company.city, current_company.street))
        _logger.info('==========')
        # TODO 需要詢問 or 增加
        _logger.info('product.name: {0}'.format('食品'))
        _logger.info('shipment date: {0}'.format(self.scheduled_date.strftime('%Y-%m-%d')))
        # TODO 需要自行增加
        _logger.info('delivery date: {0}'.format(self.scheduled_date.strftime('%Y-%m-%d')))

    def button_carrier_call(self):
        self.ensure_one()
        # 確認為物流貨運公司
        if self.carrier_id:
            if self.carrier_id.name == 'blackcat':
                # 呼叫物流貨運公司
                self.doBlackCat(self.move_ids_without_package)

        return True
