import base64
from http.client import HTTPException
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib import parse
import json
import logging

_logger = logging.getLogger(__name__)


class ApiDataEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class EcanShipOrder(object):
    # 客戶代號 String 10
    customer_no: str
    # 客戶單號 String 32 廠商出貨單號或訂單編號
    order_no: str
    # 總件數 String 3
    ttl_pcs: int
    # 規格 String 2 01:s60; 02:s90; 03:s120; 04:s150
    spec: str
    # 寄件人姓名 String 32
    sender_name: str
    # 寄件人電話 String 32
    sender_phone: str
    # 寄件人郵遞區號 String 3 郵遞區號前 3 碼
    sender_zipcode: str
    # 寄件人地址 String 64
    sender_address: str
    # 收件人姓名 String 32
    cnee_name: str
    # 收件人電話 String 32
    cnee_phone: str
    # 收件人郵遞區號 String 3 郵遞區號前 3 碼
    cnee_zipcode: str
    # 收寄人地址 String 64
    cnee_address: str
    # 希望送達日期 String 8 yyyymmdd
    hope_arrive_date: str
    # 指定時段 String 2 00:不指定;01:早;02:中
    specified_time: str
    # 代收款 String 8 若無代收款請放 0
    collection: str
    # 商品別 String 2 01:一般;02:冷凍;03 冷藏
    product_type: str
    # 作業別 String 1 1:正物流;2:逆物流
    operation_type: str
    # 備註 String 60
    remark: str
    # 代收款收款記號 String 1 0:無代收款;1:現金;2:刷卡
    collection_mark: str

    def __init__(self, customer_no: str = "",
                 order_no: str = "",
                 ttl_pcs: int = "",
                 spec: str = "",
                 sender_name: str = "",
                 sender_phone: str = "",
                 sender_zipcode: str = "",
                 sender_address: str = "",
                 cnee_name: str = "",
                 cnee_phone: str = "",
                 cnee_zipcode: str = "",
                 cnee_address: str = "",
                 hope_arrive_date: str = "",
                 specified_time: str = "",
                 collection: str = "",
                 product_type: str = "",
                 operation_type: str = "",
                 remark: str = "",
                 collection_mark: str = ""):
        self.customer_no = customer_no
        self.order_no = order_no
        self.ttl_pcs = ttl_pcs
        self.spec = spec
        self.sender_name = sender_name
        self.sender_phone = sender_phone
        self.sender_zipcode = sender_zipcode
        self.sender_address = sender_address
        self.cnee_name = cnee_name
        self.cnee_phone = cnee_phone
        self.cnee_zipcode = cnee_zipcode
        self.cnee_address = cnee_address
        self.hope_arrive_date = hope_arrive_date
        self.specified_time = specified_time
        self.collection = collection
        self.product_type = product_type
        self.operation_type = operation_type
        self.remark = remark
        self.collection_mark = collection_mark


class EcanShipOrderRequest(object):
    ship_order: List[EcanShipOrder]
    # 是否取得 PDF Boolean
    get_ship_file: bool

    def __init__(self, ship_order: List[EcanShipOrder] = None, get_ship_file: bool = True):
        self.ship_order = ship_order
        self.get_ship_file = get_ship_file


def ecan_request_ship(body: object, url: str):
    try:
        _logger.info(json.dumps(body, cls=ApiDataEncoder))
        data = json.dumps(body, cls=ApiDataEncoder).encode()
        req = Request(url, method='POST', data=data, headers={
            'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
        with urlopen(req, timeout=120) as response:
            content = response.read().decode('utf-8')
            result = json.loads(content)
            if result['code'] != 200:
                return {
                    'success': False,
                    'data': None,
                    'error': result['msg']
                }

            return {
                'success': True,
                'data': result['data'],
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


def ecan_request_zip(address: str):
    try:
        addressUriEncode = parse.quote(address)
        url = 'http://query1.e-can.com.tw:8080/Datasnap/Rest/TServerMT/LookupZip/{0}'.format(
            addressUriEncode)
        req = Request(url, method='GET', headers={
            'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
        with urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            result = json.loads(content)
            if not result['result'][0]['PZip5']:
                return {
                    'success': False,
                    'data': None,
                    'error': None
                }

            return {
                'success': True,
                'data': result['result'][0]['PZip5'][0:3],
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
