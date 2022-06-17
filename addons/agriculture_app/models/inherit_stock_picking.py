from odoo import models, fields, exceptions
import logging
from .blackcatapi import PrintObtOrder, PrintObtRequestData, request_print_obt

_logger = logging.getLogger(__name__)


class Inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    PackageName = fields.Char("PackageName", require=True)
    ShipmentDate = fields.Date("ShipmentDate", require=True)
    HopeArriveDate = fields.Date("HopeArriveDate", require=True)

    blackcat_obt_id = fields.Many2one('agriculture.blackcat_obt')

    def doBlackCat(self, packageItems):
        for item in packageItems:
            _logger.info(item.product_id)
        if not self.PackageName:
            raise exceptions.ValidationError(
                'Package name must not be empty')
        if not self.ShipmentDate:
            raise exceptions.ValidationError(
                'Shipment date must not be empty')
        if not self.HopeArriveDate:
            raise exceptions.ValidationError(
                'HopeArrive date must not be empty')
        recipientPhone = self.partner_id.Member.get_partner_attr('phone')
        if not recipientPhone:
            raise exceptions.ValidationError(
                'Recipient phone must not be empty')
        recipientAddress = self.partner_id.Member.get_partner_attr('address')
        if not recipientAddress:
            raise exceptions.ValidationError(
                'Recipient address must not be empty')

        current_company = self.env.company
        if not current_company.phone:
            raise exceptions.ValidationError(
                'Company phone must not be empty')
        senderAddress = "{0}{1}".format(
            current_company.city, current_company.street)
        if not senderAddress:
            raise exceptions.ValidationError(
                'Company address must not be empty')

        _logger.info('order id: {0}'.format(self.origin))
        _logger.info('customer.name: {0}'.format(self.partner_id.SellerName))
        _logger.info('customer.phone: {0}'.format(
            self.partner_id.Member.get_partner_attr('total-phone')))
        _logger.info('customer.address: {0}'.format(
            self.partner_id.Member.get_partner_attr('address')))
        _logger.info('==========')

        _logger.info('customer.name: {0}'.format(current_company.name))
        _logger.info('customer.phone: {0}'.format(current_company.phone))
        _logger.info('customer.address: {0}{1}'.format(
            current_company.city, current_company.street))
        _logger.info('==========')
        _logger.info('product.name: {0}'.format(self.PackageName))
        _logger.info('shipment date: {0}'.format(
            self.ShipmentDate.strftime('%Y%m%d')))
        _logger.info('delivery date: {0}'.format(
            self.HopeArriveDate.strftime('%Y%m%d')))

        orderData = PrintObtOrder(
            OrderId=self.origin,
            Thermosphere="0001",
            Spec="0004",
            ReceiptLocation="01",
            RecipientName=self.partner_id.SellerName,
            RecipientTel=recipientPhone,
            RecipientAddress=recipientAddress,
            SenderName=current_company.name,
            SenderTel=current_company.phone,
            SenderZipCode="95416E",  # TODO
            SenderAddress=senderAddress,
            ShipmentDate=self.ShipmentDate.strftime('%Y%m%d'),
            DeliveryDate=self.HopeArriveDate.strftime('%Y%m%d'),
            DeliveryTime="02",  # TODO
            IsFreight="N",
            IsCollection="N",
            CollectionAmount=0,
            IsSwipe="N",
            IsDeclare="N",
            DeclareAmount=0,
            ProductTypeId="0004",
            ProductName="Rice",
        )
        orderRequest = PrintObtRequestData(
            CustomerId="8048503301",
            CustomerToken="a9oob4cl",
            PrintOBTType="01",
            PrintType="01",
            Orders=[orderData])
        response = request_print_obt(orderRequest)
        _logger.info(response)
        # Create black obt TODO

    def button_carrier_call(self):
        self.ensure_one()
        # 確認為物流貨運公司
        if self.carrier_id:
            if self.carrier_id.name == 'blackcat':
                # 呼叫物流貨運公司
                self.doBlackCat(self.move_ids_without_package)

        return True
