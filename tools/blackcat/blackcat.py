from typing import List
from urllib.request import Request, urlopen
import json

BASE_URL_DEV = 'http://apitestsuda.southeastasia.cloudapp.azure.com:8081/api/Egs/{cmd}'
BASE_URL_PRODUCT = 'https://api.suda.com.tw/api/Egs/{cmd}'
BASE_URL = BASE_URL_DEV


class ApiDataEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Order(object):
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

    def __init__(self, OBTNumber: str = None, OrderId: int = None, Thermosphere: str = None, Spec: str = None, ReceiptLocation: str = None, ReceiptStationNo: str = None,
                 RecipientName: str = None, RecipientTel: str = None, RecipientMobile: str = None, RecipientAddress: str = None, SenderName: str = None, SenderTel: str = None,
                 SenderMobile: str = None, SenderZipCode: int = None,  SenderAddress: str = None, ShipmentDate: int = None, DeliveryDate: int = None, DeliveryTime: str = None,
                 IsFreight: str = None, IsCollection: str = None, CollectionAmount: int = None, IsSwipe: str = None, IsDeclare: str = None, DeclareAmount: int = None,
                 ProductTypeId: str = None, ProductName: str = None, Memo: str = None) -> None:
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


class PrintObtData(object):
    CustomerId: str
    CustomerToken: str
    PrintType: str
    PrintOBTType: str
    Orders: List[Order]

    def __init__(self, CustomerId: str = None, CustomerToken: str = None, PrintType: str = None, PrintOBTType: str = None, Orders: List[Order] = None) -> None:
        self.CustomerId = CustomerId
        self.CustomerToken = CustomerToken
        self.PrintType = PrintType
        self.PrintOBTType = PrintOBTType
        self.Orders = Orders


def print_obt(body):
    data = json.dumps(body, cls=ApiDataEncoder).encode()
    url_path = BASE_URL.format(cmd='PrintOBT')
    req = Request(url_path, method='POST', data=data, headers={
        'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
    with urlopen(req, timeout=120) as response:
        content = response.read().decode('utf-8')
        print(content)


if __name__ == '__main__':
    content = """{
    "CustomerId": "8048503301",
    "CustomerToken": "a9oob4cl",
    "PrintType": "01",
    "PrintOBTType": "01",
    "Orders": [
        {
            "OBTNumber": "",
            "OrderId": "12345",
            "Thermosphere": "0001",
            "Spec": "0002",
            "ReceiptLocation": "01",
            "ReceiptStationNo": "",
            "RecipientName": "test",
            "RecipientTel": "",
            "RecipientMobile": "0912123123",
            "RecipientAddress": "台北市忠孝東路五段1號1樓",
            "SenderName": "test",
            "SenderTel": "",
            "SenderMobile": "0912123123",
            "SenderZipCode": "110111",
            "SenderAddress": "台北市忠孝東路五段1號1樓",
            "ShipmentDate": "20220503",
            "DeliveryDate": "20220503",
            "DeliveryTime": "02",
            "IsFreight": "N",
            "IsCollection": "N",
            "CollectionAmount": 0,
            "IsSwipe": "N",
            "IsDeclare": "N",
            "DeclareAmount": 0,
            "ProductTypeId": "0001",
            "ProductName": "Rice",
            "Memo": ""
        }
    ]
}"""
    jObj = json.loads(content)
    data = PrintObtData(**jObj)
    print_obt(data)
