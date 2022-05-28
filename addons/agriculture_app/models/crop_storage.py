from odoo import api, models, fields
import logging


_logger = logging.getLogger(__name__)


class Storage(models.Model):
    _name = 'agriculture.storage'
    _description = 'Storage of agriculture app'
    _rec_name = 'StorageId'

    # 存放的倉庫編號 # this work 2
    StorageId = fields.Char(string='Storage Id', required=True)

    # 有StorageId的Crop # this work 2
    Crops = fields.One2many(
        'agriculture.crop', 'StorageId', string='Crops')

    # CropVariety = fields.Char(
    #     "CropVariety", compute="_ac", store=True)

    CropVarieties = fields.Char('CropVarieties')

    TotalWeight = fields.Float(
        'Total Weight', compute='_onchange_Crops', store=True)

    # @api.depends('Crops')
    # def _onchange_Crops(self):
    #     cvWeight = []
    #     cv = []
    #     for rec in self:
    #         if rec.Crops:
    #             for w in rec.Crops:
    #                 cvWeight.append(w.CropWeight)
    #                 for c in w.CropVariety:
    #                     cv.append(c.CropVariety_name)
    #     rec.TotalWeight = sum(cvWeight)
    #     rec.CropVarieties = cv

    @api.depends('Crops')
    def _onchange_Crops(self):

        for rec in self:
            cv = []
            # cvWeight = ''
            # cvWeight = []
            for c in rec.Crops:
                cv.append(c.CropVariety.CropVariety_name)
                # cv += ' ' + c.CropVariety.CropVariety_name
                # cvWeight += ' ' + str(c.CropWeight)
                # cvWeight.append(c.CropWeight)
            rec.CropVarieties = cv
        # rec.TotalWeight = cvWeight

        # _logger.info(f"this is all CropVariety_name  {cvWeight}")

    # test = fields.Char("test")

    # CropWeight = fields.Float(
    #     "CropWeight", compute="_cw", store=True)

    # @api.depends('Crops')
    # def _cw(self):
    #     res = {}
    #     for record in self:
    #         record.CropWeight = 0.0
    #         for ele in record.Crops:
    #             record.CropWeight += ele.CropWeight

    # CropVariety = fields.Char(
    #     "CropVariety", compute="_cv", store=True)

    # @api.depends('crops')
    # def _cv(self):
    #     for record in self:
    #         cv = ''
    #         for ele in record:
    #             # self.CropVariety = ele.CropVariety.CropVariety_name
    #             # cv.append(ele.CropVariety.CropVariety_name)
    #             # self.CropVariety = cv
    #             cv += ' ' + ele.CropVariety.CropVariety_name
    #             record.update({'CropVariety': cv})

    # @api.depends('Crops')
    # def _ac(self):

    #     # 所有農作物資料
    #     allCrops = self.env['agriculture.crop'].search([])
    #     # _logger.info(f"this is allCrops {allCrops}")

    #     #  所有農作物資料裡 所有不重複的StorageId
    #     StorageId_in_crops = []
    #     for rec in allCrops:
    #         StorageId_in_crops.append(rec.StorageId.StorageId)
    #     unrepeat_lists = list(set(StorageId_in_crops))
    #     # _logger.info(f"this is allStorageId  {unrepeat_lists}")

    #     my_returns = []
    #     for unrepeat_list in unrepeat_lists:
    #         # 所有農作物資料裡 所有不重複的StorageId裡 的CropVariety_name
    #         my_return = {}
    #         for record in allCrops:

    #             sId = record.search([("StorageId", "=", unrepeat_list)])
    #             CropVariety_in_crops = []
    #             CropWeight_in_crops = 0.0
    #             for ele in sId:
    #                 StorageId = ele.StorageId.StorageId
    #                 CropVariety_in_crops.append(
    #                     ele.CropVariety.CropVariety_name)
    #                 CropWeight_in_crops += ele.CropWeight

    #             my_return = {
    #                 "storage_id": StorageId,
    #                 "crop_variety": CropVariety_in_crops,
    #                 "crop_weight": CropWeight_in_crops
    #             }

    #         # _logger.info(
    #         #     f"this is single = {my_return}")

    #         my_returns.append(my_return)

    #     _logger.info(
    #         f"this is all  = {my_returns}")

        # for r in self:
        #     r.CropVariety = my_return
        #     r.test = my_return['storage_id']
        #     _logger.info(f"this is {r.test}")
