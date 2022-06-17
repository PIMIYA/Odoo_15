from typing import List
from urllib.request import Request, urlopen
import json

BASE_URL_DEV = 'http://apitestsuda.southeastasia.cloudapp.azure.com:8081/api/Egs/{cmd}'
BASE_URL_PRODUCT = 'https://api.suda.com.tw/api/Egs/{cmd}'
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


def request_print_obt(body: PrintObtRequestData):
    data = json.dumps(body, cls=ApiDataEncoder).encode()
    url_path = BASE_URL.format(cmd='PrintOBT')
    req = Request(url_path, method='POST', data=data, headers={
        'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
    try:
        with urlopen(req, timeout=120) as response:
            content = response.read().decode('utf-8')
            result = json.loads(content)
            return {
                'success': True,
                'data': result,
                'error': None
            }
    except Exception as error:
        return {
            'success': False,
            'data': None,
            'error': error.reason()
        }
