from odoo import http


class Crops(http.Controller):

    @http.route("/agriculture/crops")
    def list(self, **kwargs):
        Crop = http.request.env["agriculture.crop"]
        crops = Crop.search([])
        return http.request.render(
            "agriculture_app.crop_list_template",
            {"crops": crops}
        )
# -*- coding: utf-8 -*-
# from odoo import http


# class Dolimi(http.Controller):
#     @http.route('/dolimi/dolimi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dolimi/dolimi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dolimi.listing', {
#             'root': '/dolimi/dolimi',
#             'objects': http.request.env['dolimi.dolimi'].search([]),
#         })

#     @http.route('/dolimi/dolimi/objects/<model("dolimi.dolimi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dolimi.object', {
#             'object': obj
#         })
