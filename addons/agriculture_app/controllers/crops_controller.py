from odoo import http, _, exceptions
import json
import logging

from .serializers import Serializer
from .exceptions import QueryFormatError


_logger = logging.getLogger(__name__)


def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }


class Crops(http.Controller):

    # get a single crop record
    @http.route('/api/v1/agriculture/crop/rec', type='http', auth="public", methods=['POST'], csrf=False)
    def get_crop_record(self, **kwargs):
        seq = kwargs.get('SeqNumber')
        try:
            record = http.request.env['agriculture.crop'].sudo().search(
                [('SeqNumber', '=', seq)]).ensure_one()
        except KeyError as e:
            msg = "The record `%s` does not exist." % seq
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

        try:
            serializer = Serializer(record)
            data = serializer.data
        except (SyntaxError, QueryFormatError) as e:
            res = error_response(e, e.msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

        # _logger.info("Successfully get the record `%s`." % data)

        # replace many2one field index to String
        #
        data['SellerName'] = record.SellerName.SellerName
        data['CropVariety'] = record.CropVariety.CropVariety_name
        res = {
            "result": data
        }

        return http.Response(
            json.dumps(res),
            status=200,
            mimetype='application/json'
        )

    # create a new record

    @http.route('/api/v1/agriculture/crop/', type='json', auth="public", methods=['POST'], csrf=False)
    def post_crop_record(self, **kwargs):
        try:
            data = kwargs['data']
        except KeyError as e:
            msg = "`data` parameter is not found on POST request body"
            raise exceptions.ValidationError(msg)

        try:
            rec_to_post = http.request.env['agriculture.crop']
        except KeyError:
            msg = "The model `%s` does not exist." % rec_to_post
            raise exceptions.ValidationError(msg)

        check = rec_to_post.sudo().search(
            [('SeqNumber', '=', data['SeqNumber'])])

        # _logger.info("test: %s" % test)
        if check:
            msg = "The record `%s` already exists." % data['SeqNumber']
            raise exceptions.ValidationError(msg)
        else:
            if "context" in kwargs:
                context = kwargs["context"]
                record = rec_to_post.with_context(
                    **context).sudo().create(data)
            else:
                record = rec_to_post.sudo().create(data)
                return record.id

    # update a record

    @http.route('/api/v1/agriculture/crop/<int:seqNumber>', type='json', auth="public", methods=['PUT'], csrf=False)
    def put_crop_record(self, seqNumber, **kwargs):
        try:
            data = kwargs['data']
            m_data = kwargs['member']
            c_data = kwargs['cropvariety']
        except KeyError:
            msg = "`data` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)

        try:
            rec_to_put = http.request.env['agriculture.crop']
        except KeyError:
            msg = "The model `%s` does not exist." % rec_to_put
            raise exceptions.ValidationError(msg)

        member_id = 0
        cropvariety_id = 0

        check_member = rec_to_put.SellerName.sudo().search(
            [('SellerName', '=', m_data['SellerName'])])

        if not check_member:
            member_id = check_member.sudo().create(m_data).id
        else:
            member_id = check_member.ensure_one().id
            _logger.info("member id is `%s` " % member_id)
            member = rec_to_put.SellerName.sudo().browse(member_id)
            _logger.info("member is `%s` " % member['SellerName'])

        check_cropvariety = rec_to_put.CropVariety.sudo().search(
            [('CropVariety_name', '=', c_data['CropVariety_name'])])

        if not check_cropvariety:
            cropvariety_id = check_cropvariety.sudo().create(c_data).id
        else:
            cropvariety_id = check_cropvariety.ensure_one().id
            _logger.info("cropvariety id is `%s` " % cropvariety_id)
            cropvariety = rec_to_put.CropVariety.sudo().browse(cropvariety_id)
            _logger.info("cropvariety is `%s` " %
                         cropvariety['CropVariety_name'])

        check_record = rec_to_put.sudo().search(
            [('SeqNumber', '=', seqNumber)])

        if not check_record:
            msg = "The record `%s` not exists." % seqNumber
            raise exceptions.ValidationError(msg)

        else:
            try:
                data['SellerName'] = member_id
                data['CropVariety'] = cropvariety_id
                return check_record.sudo().write(data)
            except Exception as e:
                return False
