# -*- coding: utf-8 -*-
from odoo import http


class AgricultureMember(http.Controller):
    @http.route('/agriculture_member/agriculture_member/objects', auth='public')
    def list(self, **kw):
        return http.request.render('agriculture_member.listing', {
            'root': '/agriculture_member/agriculture_member',
            'objects': http.request.env['agriculture_app.member'].search([]),
        })

    @http.route('/agriculture_member/agriculture_member/objects/<model("agriculture_app.member"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('agriculture_member.object', {
            'object': obj
        })
