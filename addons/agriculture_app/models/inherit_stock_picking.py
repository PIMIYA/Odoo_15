from odoo import models, fields, api, exceptions
import logging
from .blackcatapi import PrintObtOrder, PrintObtRequestData, SearchAddress, AddressRequestData, ShippingPdfRequestData, \
    get_zipcode, request_print_obt, request_address, request_pdf

_logger = logging.getLogger(__name__)


DefinedBlackcatState = [
    ('none', 'None'),
    ('obtRequested', 'OBT Requested'),
]


class Inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    BlackcatObtId = fields.One2many(
        'agriculture.blackcat_obt', 'StockPickingId', 'Blackcat OBT')
    BlackcatState = fields.Selection(
        DefinedBlackcatState, 'State', default=DefinedBlackcatState[0][0])

    PackageName = fields.Char("PackageName", require=True)
    ShipmentDate = fields.Date("ShipmentDate", require=True)
    HopeArriveDate = fields.Date("HopeArriveDate", require=True)

    def requestBlackCat(self, packageItems):
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
        recipientPhone = self.partner_id.Member.get_partner_attr(
            'mobile-or-phone')
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

        # _logger.info('order id: {0}'.format(self.origin))
        # _logger.info('customer.name: {0}'.format(self.partner_id.SellerName))
        # _logger.info('customer.phone: {0}'.format(
        #     self.partner_id.Member.get_partner_attr('total-phone')))
        # _logger.info('customer.address: {0}'.format(
        #     self.partner_id.Member.get_partner_attr('address')))
        # _logger.info('==========')

        # _logger.info('customer.name: {0}'.format(current_company.name))
        # _logger.info('customer.phone: {0}'.format(current_company.phone))
        # _logger.info('customer.address: {0}{1}'.format(
        #     current_company.city, current_company.street))
        # _logger.info('==========')
        # _logger.info('product.name: {0}'.format(self.PackageName))
        # _logger.info('shipment date: {0}'.format(
        #     self.ShipmentDate.strftime('%Y%m%d')))
        # _logger.info('delivery date: {0}'.format(
        #     self.HopeArriveDate.strftime('%Y%m%d')))

        # TODO
        customerId = str("8048503301")
        # TODO
        customerToken = str("a9oob4cl")
        productName = self.PackageName

        searchAddress = SearchAddress(Search=senderAddress)
        addressRequest = AddressRequestData(
            CustomerId=customerId,
            CustomerToken=customerToken,
            Addresses=[searchAddress]
        )

        zipCode = str('')
        addressResponse = request_address(addressRequest)
        if addressResponse['success']:
            # Create black obt
            addressResData = addressResponse['data']
            # _logger.info(addressResData)
            if not addressResData:
                raise exceptions.ValidationError(
                    'Address Response data is null')
            postNumber = addressResData['Data']['Addresses'][0]['PostNumber']
            zipCode = get_zipcode(postNumber=postNumber)
        else:
            raise exceptions.ValidationError(addressResponse['error'])

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
            SenderZipCode=zipCode,
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
            ProductName=productName,
        )
        orderRequest = PrintObtRequestData(
            CustomerId=customerId,
            CustomerToken=customerToken,
            PrintOBTType="01",
            PrintType="01",
            Orders=[orderData])
        orderReponse = request_print_obt(orderRequest)
        # _logger.info(response)
        if orderReponse['success']:
            # Create black obt
            data = orderReponse['data']
            # _logger.info(data)
            if not data:
                raise exceptions.ValidationError(
                    'Print Obt Response data is null')

            pdfRequestData = ShippingPdfRequestData(
                CustomerId=customerId,
                CustomerToken=customerToken,
                FileNo=data['Data']['FileNo']
            )
            binaryData = request_pdf(pdfRequestData)

            self.write({'BlackcatObtId': [
                (0, 0, {
                    'SrvTranId': data['SrvTranId'],
                    'OBTNumber': data['Data']['Orders'][0]['OBTNumber'],
                    'FileNo': pdfRequestData.FileNo,
                    'ShippingPdf': binaryData,
                    'StockPickingId': self
                })
            ]})
            pass
        else:
            raise exceptions.ValidationError(orderReponse['error'])

    def button_carrier_call(self):
        self.ensure_one()
        # 確認為物流貨運公司
        if self.carrier_id:
            if self.carrier_id.name == 'blackcat':
                # 呼叫物流貨運公司
                self.requestBlackCat(self.move_ids_without_package)

        return True

    @api.model
    def create(self, vals):
        self.env.cr.commit()
        return super(Inherit_stock_picking, self).create(vals)
