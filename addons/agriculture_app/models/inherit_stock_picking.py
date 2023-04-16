from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
from datetime import timedelta, date
from lxml import etree
import logging
from .blackcatapi import PrintObtOrder, PrintObtRequestData, SearchAddress, AddressRequestData, ShippingPdfRequestData, \
    get_zipcode, request_print_obt, request_address, request_pdf
from .ecan import EcanShipOrder, EcanShipOrderRequest, ecan_request_ship, ecan_request_zip
from .helper import get_phone_info, get_address_info, get_company_phone, get_company_address

_logger = logging.getLogger(__name__)

DefinedBShippState = [
    ('none', 'None'),
    ('obtRequested', 'OBT Requested'),
    ('printRequested', 'Print Requested'),
]


class Inherit_stock_picking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    BlackcatObtId = fields.Many2one(
        'agriculture.blackcat_obt', compute='compute_blackcat_obt', inverse='blackcat_obt_inverse')
    BlackcatObtIds = fields.One2many(
        'agriculture.blackcat_obt', 'StockPickingId', 'Blackcat OBT')
    ShippingState = fields.Selection(
        DefinedBShippState, 'State', default=DefinedBShippState[0][0])

    # '''需新增packageName對應至商品分類項目'''
    # PackageName = fields.Char(
    #     "PackageName", require=True)
    ShipmentDate = fields.Date(
        "ShipmentDate", require=True, default=date.today())
    HopeArriveDate = fields.Date(
        "HopeArriveDate", require=True, default=date.today() + timedelta(days=3))

    Shipping_method = fields.Char(
        'Shipping_method', default='')

    Shipping_destination = fields.Char('Shipping_destination', default='')

    temp_conpany_phone = fields.Char('temp_conpany_phone', default='')

    @api.depends('BlackcatObtIds')
    def compute_blackcat_obt(self):
        idx = len(self.BlackcatObtIds)
        if idx > 0:
            self.BlackcatObtId = self.BlackcatObtIds[idx - 1]

    def blackcat_obt_inverse(self):
        idx = len(self.BlackcatObtIds)
        if idx > 0:
            # delete previous reference
            asset = self.env['agriculture.blackcat_obt'].browse(
                self.BlackcatObtIds[0].id)
            asset.StockPickingId = False
        # set new reference
        self.BlackcatObtId.StockPickingId = self

    def create_notification(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Success'),
                'type': 'success',
                'sticky': False,
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }

    def no_carrier_notification(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('no carrier selected!'),
                'type': 'success',
                'sticky': False,
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }

    def requestBlackCat(self, packageItems):
        # if not self.PackageName:
        #     raise exceptions.ValidationError(
        #         'Package name must not be empty')
        if not self.ShipmentDate:
            raise exceptions.ValidationError(
                'Shipment date must not be empty')
        if not self.HopeArriveDate:
            raise exceptions.ValidationError(
                'HopeArrive date must not be empty')
        # recipientPhone = self.partner_id.Member.get_partner_attr(
        #     'mobile-or-phone').replace('+88
        # 6', '0').replace(" ", "")
        # if self.partner_id.mobile:
        #     if self.partner_id.mobile.startswith('+886'):
        #         recipientPhone = self.partner_id.mobile.replace(
        #             '+886', '0').replace(" ", "")
        #     else:
        #         recipientPhone = self.partner_id.mobile
        # else:
        #     if self.partner_id.phone.startswith('+886'):
        #         recipientPhone = self.partner_id.phone.replace(
        #             '+886', '0').replace(" ", "")
        #     else:
        #         recipientPhone = self.partner_id.phone
        recipientPhone = get_phone_info(self.partner_id)
        # _logger.info('recipientPhone: %s', recipientPhone)
        if not recipientPhone:
            raise exceptions.ValidationError(
                'Recipient phone must not be empty')
        # recipientAddress = self.partner_id.Member.get_partner_attr('address')
        # recipientAddress = self.partner_id.contact_address
        # if self.partner_id.street2:
        #     if self.partner_id.state_id.name == self.partner_id.city:
        #         recipientAddress = "{0}{1}{2}{3}".format(
        #             self.partner_id.zip, self.partner_id.state_id.name, self.partner_id.street, self.partner_id.street2)
        #     else:
        #         recipientAddress = "{0}{1}{2}{3}{4}".format(
        #             self.partner_id.zip, self.partner_id.state_id.name, self.partner_id.city, self.partner_id.street,
        #             self.partner_id.street2)
        # else:
        #     if self.partner_id.state_id.name == self.partner_id.city:
        #         recipientAddress = "{0}{1}{2}".format(
        #             self.partner_id.zip, self.partner_id.state_id.name, self.partner_id.street)
        #     else:
        #         recipientAddress = "{0}{1}{2}{3}".format(
        #             self.partner_id.zip, self.partner_id.state_id.name, self.partner_id.city, self.partner_id.street)
        recipientAddress = get_address_info(self.partner_id)
        # _logger.info('recipientAddress: %s', recipientAddress)
        if not recipientAddress:
            raise exceptions.ValidationError(
                'Recipient address must not be empty')

        current_company = self.env.company
        if not current_company.phone:
            raise exceptions.ValidationError(
                'Company phone must not be empty')
        senderAddress = get_company_address(current_company)
        _logger.info('senderAddress: %s', senderAddress)
        if not senderAddress:
            raise exceptions.ValidationError(
                'Company address must not be empty')
        senderPhone = get_company_phone(current_company)
        _logger.info('senderPhone: %s', senderPhone)
        if not senderPhone:
            raise exceptions.ValidationError(
                'Company phone must not be empty')
        self.temp_conpany_phone = senderPhone

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

        # _logger.info('phone: {0}'.format(recipientPhone))
        # _logger.info('company_phone: {0}'.format(
        #     current_company.phone.replace('+886', '0').replace(" ", "")))

        config = self.env['ir.config_parameter'].sudo()
        customerId = config.get_param('agriculture.blackCat_customer_id')
        customerToken = config.get_param('agriculture.blackCat_api_token')
        apiBaseUrl = config.get_param('agriculture.blackCat_api_url')
        if not customerId:
            raise exceptions.ValidationError('請設定黑貓客戶編號')
        if not customerToken:
            raise exceptions.ValidationError('請設定黑貓授權碼')
        if not apiBaseUrl:
            raise exceptions.ValidationError('請設定黑貓 API URL')

        # 預設商品名稱
        products = ''
        for record in self.move_line_ids_without_package:
            products += record.product_id.name + ' '
            _logger.info('product: %s', products)
        productName = products
        note = ''

        searchAddress = SearchAddress(Search=senderAddress)
        addressRequest = AddressRequestData(
            CustomerId=customerId,
            CustomerToken=customerToken,
            Addresses=[searchAddress]
        )

        zipCode = str('')
        addressResponse = request_address(apiBaseUrl, addressRequest)
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
            # RecipientName=self.partner_id.SellerName,
            RecipientName=self.partner_id.name,
            RecipientTel=recipientPhone,
            RecipientAddress=recipientAddress,
            SenderName=current_company.name,
            SenderTel=self.temp_conpany_phone,
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
            ProductTypeId="0001",
            ProductName=productName,
            Memo=note
        )
        orderRequest = PrintObtRequestData(
            CustomerId=customerId,
            CustomerToken=customerToken,
            PrintOBTType="01",
            PrintType="01",
            Orders=[orderData])
        orderReponse = request_print_obt(apiBaseUrl, orderRequest)
        # _logger.info(response)
        if orderReponse['success']:
            self.ShippingState = DefinedBShippState[1][0]
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
            binaryData = request_pdf(apiBaseUrl, pdfRequestData)

            self.write({'BlackcatObtIds': [
                (0, 0, {
                    'SrvTranId': data['SrvTranId'],
                    'OBTNumber': data['Data']['Orders'][0]['OBTNumber'],
                    'FileNo': pdfRequestData.FileNo,
                    'ShippingPdf': binaryData,
                    'StockPickingId': self
                })
            ]})
            self.ShippingState = DefinedBShippState[2][0]

            return True
        else:
            raise exceptions.ValidationError(orderReponse['error'])

    def requestECan(self, packageItems):
        # prepare api request data
        if not self.ShipmentDate:
            raise exceptions.ValidationError(
                'Shipment date must not be empty')
        if not self.HopeArriveDate:
            raise exceptions.ValidationError(
                'HopeArrive date must not be empty')
        recipientName = self.partner_id.name,
        recipientPhone = get_phone_info(self.partner_id)
        # _logger.info('recipientPhone: %s', recipientPhone)
        if not recipientPhone:
            raise exceptions.ValidationError(
                'Recipient phone must not be empty')
        recipientAddress = get_address_info(self.partner_id)
        # _logger.info('recipientAddress: %s', recipientAddress)
        if not recipientAddress:
            raise exceptions.ValidationError(
                'Recipient address must not be empty')

        current_company = self.env.company
        senderName = current_company.name
        senderAddress = get_company_address(current_company)
        _logger.info('senderAddress: %s', senderAddress)
        if not senderAddress:
            raise exceptions.ValidationError(
                'Company address must not be empty')
        senderPhone = get_company_phone(current_company)
        _logger.info('senderPhone: %s', senderPhone)
        if not senderPhone:
            raise exceptions.ValidationError(
                'Company phone must not be empty')
        self.temp_conpany_phone = senderPhone

        # 商品名稱、數量
        productName = ''
        productCount = 0
        for record in self.move_line_ids_without_package:
            productCount += 1
            productName += record.product_id.name + ' '
        # _logger.info('productName: %s', productName)
        # _logger.info('productCount: %s', productCount)

        recipientZipResponse = ecan_request_zip(recipientAddress)
        # _logger.info('recipientZipResponse: %s', recipientZipResponse)
        if not recipientZipResponse['success']:
            raise exceptions.ValidationError(
                '收件者地址取得區碼錯誤, {0}'.format(recipientZipResponse['error']))
        recipientZip = recipientZipResponse['data']
        senderZipResponse = ecan_request_zip(senderAddress)
        # _logger.info('senderZipResponse: %s', senderZipResponse)
        if not senderZipResponse['success']:
            raise exceptions.ValidationError(
                '收件者地址取得區碼錯誤, {0}'.format(senderZipResponse['error']))
        senderZip = senderZipResponse['data']

        order_no = self.origin
        _logger.info("order_no: %s", order_no)
        hopeArriveDate = self.HopeArriveDate.strftime('%Y%m%d')
        _logger.info("hopeArriveDate: %s", hopeArriveDate)

        # process response
        config = self.env['ir.config_parameter'].sudo()
        customerId = config.get_param('agriculture.ecan_customer_id')
        apiBaseUrl = config.get_param('agriculture.ecan_api_url')
        if not customerId:
            raise exceptions.ValidationError('請設定宅配通客戶編號')
        if not apiBaseUrl:
            raise exceptions.ValidationError('請設定宅配通 API URL')

        ecanShipOrder = EcanShipOrder(
            customer_no=customerId,
            order_no=order_no,
            ttl_pcs=productCount,
            spec="04",  # TODO 01, 02, 03, 04?
            sender_name=senderName,
            sender_phone=senderPhone,
            sender_address=senderAddress,
            sender_zipcode=senderZip,
            cnee_name=recipientName,
            cnee_phone=recipientPhone,
            cnee_zipcode=recipientZip,
            cnee_address=recipientAddress,
            hope_arrive_date=hopeArriveDate,
            specified_time="00",
            collection="0",
            product_type="01",
            operation_type="1",
            remark="",
            collection_mark="0"
        )
        ecanShipOrderRequest = EcanShipOrderRequest(ship_order=[ecanShipOrder])
        response = ecan_request_ship(ecanShipOrderRequest, apiBaseUrl)
        _logger.info("response: %s", response)
        if response['success']:
            data = response['data']
            if not data:
                raise exceptions.ValidationError(
                    'e-can Response data is null')
            shippingData = data['successData']
            if not shippingData:
                raise exceptions.ValidationError(
                    'e-can shipping data is null')
            pdfUrl = data['pdfDownloadUrl']
            # TODO: create e-can obt?
            # self.write({'BlackcatObtIds': [
            #     (0, 0, {
            #         'SrvTranId': data['SrvTranId'],
            #         'OBTNumber': data['Data']['Orders'][0]['OBTNumber'],
            #         'FileNo': pdfRequestData.FileNo,
            #         'ShippingPdf': binaryData,
            #         'StockPickingId': self
            #     })
            # ]})

            # 直接用 ShippingState
            # self.ShippingState = DefinedBShippState[1][0]
            # self.ShippingState = DefinedBShippState[2][0]
            # return True
        else:
            raise exceptions.ValidationError(response['error'])

    def button_carrier_call(self):
        self.ensure_one()
        # 確認為物流貨運公司
        if self.carrier_id:
            if self.carrier_id.name in ('Blackcat', '黑貓宅急便'):
                # 呼叫物流貨運公司
                if self.requestBlackCat(self.move_ids_without_package):
                    return self.create_notification()
            if self.carrier_id.name == 'e-can' or '宅配通':
                # 呼叫物流貨運公司
                if self.requestECan(self.move_ids_without_package):
                    return self.create_notification()

            return self.no_carrier_notification()
        else:
            return self.no_carrier_notification()
        return True

    @api.onchange('carrier_id')
    def _onchange_(self):
        for rec in self:
            rec.Shipping_method = self.carrier_id.name
            rec.Shipping_destination = self.partner_id.state_id.name
            _logger.info(f"carrier_id name: {rec.Shipping_method}")

    @api.depends('Shipping_method')
    def _compute_shipping_method(self):
        for rec in self:
            rec.Shipping_method = self.carrier_id.name
            rec.Shipping_destination = self.partner_id.state_id.name
            _logger.info(f"carrier_id name: {rec.Shipping_method}")

    @api.model
    def create(self, vals):
        self.env.cr.commit()
        return super(Inherit_stock_picking, self).create(vals)

    def default_get(self, fields):
        res = super(Inherit_stock_picking, self).default_get(fields)
        res['Shipping_method'] = self.carrier_id.name
        res['Shipping_destination'] = self.partner_id.state_id.name
        return res
