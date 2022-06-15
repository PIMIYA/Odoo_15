from pkg_resources import require
from odoo import models, fields, api, exceptions
import logging

_logger = logging.getLogger(__name__)


class Inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    PackageName = fields.Char("PackageName", require=True)
    ShipmentDate = fields.Date("ShipmentDate", require=True)
    HopeArriveDate = fields.Date("HopeArriveDate", require=True)

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
        if not self.PackageName:
            raise exceptions.ValidationError(
                'Package name must not be empty')
        if not self.ShipmentDate:
            raise exceptions.ValidationError(
                'Shipment date must not be empty')
        if not self.HopeArriveDate:
            raise exceptions.ValidationError(
                'HopeArrive date must not be empty')

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
        _logger.info('product.name: {0}'.format(self.PackageName))
        _logger.info('shipment date: {0}'.format(
            self.ShipmentDate.strftime('%Y-%m-%d')))
        _logger.info('delivery date: {0}'.format(
            self.HopeArriveDate.strftime('%Y-%m-%d')))

    def button_carrier_call(self):
        self.ensure_one()
        # 確認為物流貨運公司
        if self.carrier_id:
            if self.carrier_id.name == 'blackcat':
                # 呼叫物流貨運公司
                self.doBlackCat(self.move_ids_without_package)

        return True
