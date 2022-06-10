from odoo import models, fields, api


class Inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    def button_carrier_call(self):
        self.ensure_one()
        #確認為物流貨運公司
        if self.carrier_id:
            #呼叫物流貨運公司
            pass

        return True