import base64
from http.client import HTTPException
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import logging

_logger = logging.getLogger(__name__)

BASE_URL_DEV = 'http://apitestsuda.southeastasia.cloudapp.azure.com:8081/api/egs/{cmd}'
BASE_URL_PRODUCT = 'https://api.suda.com.tw/api/egs/{cmd}'
BASE_URL = BASE_URL_DEV


class ApiDataEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class PrintObtOrder(object):
    OBTNumber: str
    OrderId: int
    Thermosphere: str
    Spec: str
    ReceiptLocation: str
    ReceiptStationNo: str
    RecipientName: str
    RecipientTel: str
    RecipientMobile: str
    RecipientAddress: str
    SenderName: str
    SenderTel: str
    SenderMobile: str
    SenderZipCode: int
    SenderAddress: str
    ShipmentDate: int
    DeliveryDate: int
    DeliveryTime: str
    IsFreight: str
    IsCollection: str
    CollectionAmount: int
    IsSwipe: str
    IsDeclare: str
    DeclareAmount: int
    ProductTypeId: str
    ProductName: str
    Memo: str

    def __init__(self, OBTNumber: str = "", OrderId: int = None, Thermosphere: str = "", Spec: str = "", ReceiptLocation: str = "", ReceiptStationNo: str = "",
                 RecipientName: str = "", RecipientTel: str = "", RecipientMobile: str = "", RecipientAddress: str = "", SenderName: str = "", SenderTel: str = "",
                 SenderMobile: str = "", SenderZipCode: int = None,  SenderAddress: str = "", ShipmentDate: int = None, DeliveryDate: int = None, DeliveryTime: str = "",
                 IsFreight: str = "", IsCollection: str = "", CollectionAmount: int = None, IsSwipe: str = "", IsDeclare: str = "", DeclareAmount: int = None,
                 ProductTypeId: str = "", ProductName: str = "", Memo: str = ""):
        self.OBTNumber = OBTNumber
        self.OrderId = OrderId
        self.Thermosphere = Thermosphere
        self.Spec = Spec
        self.ReceiptLocation = ReceiptLocation
        self.ReceiptStationNo = ReceiptStationNo
        self.RecipientName = RecipientName
        self.RecipientTel = RecipientTel
        self.RecipientMobile = RecipientMobile
        self.RecipientAddress = RecipientAddress
        self.SenderName = SenderName
        self.SenderTel = SenderTel
        self.SenderMobile = SenderMobile
        self.SenderZipCode = SenderZipCode
        self.SenderAddress = SenderAddress
        self.ShipmentDate = ShipmentDate
        self.DeliveryDate = DeliveryDate
        self.DeliveryTime = DeliveryTime
        self.IsFreight = IsFreight
        self.IsCollection = IsCollection
        self.CollectionAmount = CollectionAmount
        self.IsSwipe = IsSwipe
        self.IsDeclare = IsDeclare
        self.DeclareAmount = DeclareAmount
        self.ProductTypeId = ProductTypeId
        self.ProductName = ProductName
        self.Memo = Memo


class PrintObtRequestData(object):
    CustomerId: str
    CustomerToken: str
    PrintType: str
    PrintOBTType: str
    Orders: List[PrintObtOrder]

    def __init__(self, CustomerId: str = "",
                 CustomerToken: str = "",
                 PrintType: str = "",
                 PrintOBTType: str = "",
                 Orders: List[PrintObtOrder] = None):
        self.CustomerId = CustomerId
        self.CustomerToken = CustomerToken
        self.PrintType = PrintType
        self.PrintOBTType = PrintOBTType
        self.Orders = Orders


class SearchAddress(object):
    Search: str

    def __init__(self, Search: str):
        self.Search = Search


class AddressRequestData(object):
    CustomerId: str
    CustomerToken: str
    Addresses: List[SearchAddress]

    def __init__(self, CustomerId: str = "",
                 CustomerToken: str = "",
                 Addresses: List[SearchAddress] = None):
        self.CustomerId = CustomerId
        self.CustomerToken = CustomerToken
        self.Addresses = Addresses


class ShippingPdfRequestData(object):
    CustomerId: str
    CustomerToken: str
    FileNo: str

    def __init__(self, CustomerId: str = f"",
                 CustomerToken: str = f"",
                 FileNo: str = f""):
        self.CustomerId = CustomerId
        self.CustomerToken = CustomerToken
        self.FileNo = FileNo


def get_zipcode(postNumber: str):
    return postNumber.replace("-", "")[-6:]


def blackcat_request(body: object, requestCmd: str):
    try:
        data = json.dumps(body, cls=ApiDataEncoder).encode()
        url_path = BASE_URL.format(cmd=requestCmd)
        req = Request(url_path, method='POST', data=data, headers={
            'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
        with urlopen(req, timeout=120) as response:
            content = response.read().decode('utf-8')
            result = json.loads(content)
            if result['IsOK'] != 'Y':
                return {
                    'success': False,
                    'data': None,
                    'error': result['Message']
                }

            return {
                'success': True,
                'data': result,
                'error': None
            }
    except HTTPError as error:
        return {
            'success': False,
            'data': None,
            'error': f"Http error {error.code=}"
        }
    except URLError as error:
        return {
            'success': False,
            'data': None,
            'error': error.reason
        }
    except Exception as error:
        return {
            'success': False,
            'data': None,
            'error': f"Unexpected {error=}, {type(error)=}"
        }


def request_print_obt(body: PrintObtRequestData):
    requestCmd = f"PrintOBT"
    return blackcat_request(body=body, requestCmd=requestCmd)


def request_address(body: AddressRequestData):
    requestCmd = f"ParsingAddress"
    return blackcat_request(body=body, requestCmd=requestCmd)


def request_pdf(body: ShippingPdfRequestData):
    requestCmd = f"DownloadOBT"
    try:
        data = json.dumps(body, cls=ApiDataEncoder).encode()
        url_path = BASE_URL.format(cmd=requestCmd)
        req = Request(url_path, method='POST', data=data, headers={
            'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
        with urlopen(req, timeout=120) as response:
            content = response.read()
            return base64.b64encode(content)
    except HTTPError as error:
        return {
            'success': False,
            'data': None,
            'error': f"Http error {error.code=}"
        }
    except URLError as error:
        return {
            'success': False,
            'data': None,
            'error': error.reason
        }
    except Exception as error:
        return {
            'success': False,
            'data': None,
            'error': f"Unexpected {error=}, {type(error)=}"
        }
