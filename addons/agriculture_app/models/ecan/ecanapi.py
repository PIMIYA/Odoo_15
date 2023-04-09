import base64
from http.client import HTTPException
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import logging

_logger = logging.getLogger(__name__)


class ApiDataEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class EcanShipOrder(object):
    customer_no: str
    order_no: str
    ttl_pcs: int
    spec: str
    sender_name: str
    sender_phone: str
    sender_zipcode: str
    sender_address: str
    cnee_name: str
    cnee_phone: str
    cnee_zipcode: str
    cnee_address: str
    hope_arrive_date: str
    specified_time: str
    collection: str
    product_type: str
    operation_type: str
    remark: str
    collection_mark: str

    def __int__(self, customer_no: str = "",
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
    get_ship_file: bool


def ecan_request(body: object, url: str):
    try:
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
