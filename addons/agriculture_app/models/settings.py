from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class Preferences(models.TransientModel):
    _inherit = 'res.config.settings'

    currency_id = fields.Many2one(
        'res.currency', string='Currency')

    # Fields
    # ----------------------------------------------------------
    # General
    BasePrice = fields.Monetary(
        string='Base Price', options="{'currency_field': 'currency_id'}", required=True, default=1400.0)

    ContractedMemberPrice = fields.Monetary(
        'Contracted Member Price', required=True, default=150.0, options="{'currency_field': 'currency_id'}")
    KoshihikariRice = fields.Monetary(
        'Koshihikari Rice', default=1050.0, required=True, options="{'currency_field': 'currency_id'}")
    GlutinousRicePrice_BR = fields.Monetary(
        'Glutinous Rice Price BR', default=850.0, required=True, options="{'currency_field': 'currency_id'}")
    GlutinousRicePrice = fields.Monetary(
        'Glutinous Rice Price', default=150.0, required=True, options="{'currency_field': 'currency_id'}")

    OrganicRice = fields.Monetary(
        'Organic Rice', default=750.0, required=True, options="{'currency_field': 'currency_id'}")
    VolumeWeightIsOverAndEqualTo = fields.Float(
        'Volume Weight Is Over And Equal To', default=620.0)
    PrimeYieldIsOverAndEqualTo = fields.Float(
        'Prime Yield Is Over And Equal To', default=70.0)
    OrganicRiceExtra = fields.Monetary(
        'Organic Rice Extra', default=300.0, required=True, options="{'currency_field': 'currency_id'}")

    OrganicTransOrIso = fields.Monetary(
        'OrganicTransOrIso', default=650.0, required=True, options="{'currency_field': 'currency_id'}")

    # first stage conditions
    # ----------------------------------------------------------
    fs_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=620.0)
    fs_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=73.0)
    fs_BrownIntactRatioIsOver = fields.Integer(
        'Brown Intact Ratio Is Over', default=80)

    fs_bonus = fields.Monetary(
        'fs_bonus', default=180.0, required=True, options="{'currency_field': 'currency_id'}")

    # second stage conditions
    # ----------------------------------------------------------
    ss_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=590.0)
    ss_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=65.0)
    ss_BrownIntactRatioIsOver = fields.Integer(
        'Brown Intact Ratio Is Over', default=70)

    ss_bonus = fields.Monetary(
        'ss_bonus', default=120.0, required=True, options="{'currency_field': 'currency_id'}")

    # third stage conditions
    # ----------------------------------------------------------
    ts_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=560.0)
    ts_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=64.0)
    ts_BrownIntactRatioIsOver = fields.Integer(
        'Brown Intact Ratio Is Over', default=65)

    ts_bonus = fields.Monetary(
        'ts_bonus', default=60.0, required=True, options="{'currency_field': 'currency_id'}")

    # fourth stage conditions
    # ----------------------------------------------------------
    ffs_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=539.0)
    ffs_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=59.0)
    ffs_BrownIntactRatioIsOver = fields.Integer(
        'Brown Intact Ratio Is Over', default=60)

    # TGAP bonus
    # ----------------------------------------------------------
    tgap_bonus = fields.Monetary(
        'TGAP bonus', default=100.0, required=True, options="{'currency_field': 'currency_id'}")

    final_PrimeYieldIsOverAndEqualTo = fields.Float(
        'Prime Yield Is Over And Equal To', default=70.0)

    # Final multiplication
    # ----------------------------------------------------------
    multiplication = fields.Integer('Multiplication', default=20)

    def set_values(self):
        """agriculture setting field values"""
        res = super(Preferences, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'agriculture.BasePrice', self.BasePrice)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ContractedMemberPrice', self.ContractedMemberPrice)
        self.env['ir.config_parameter'].set_param(
            'agriculture.KoshihikariRice', self.KoshihikariRice)
        self.env['ir.config_parameter'].set_param(
            'agriculture.GlutinousRicePrice_BR', self.GlutinousRicePrice_BR)
        self.env['ir.config_parameter'].set_param(
            'agriculture.GlutinousRicePrice', self.GlutinousRicePrice)
        self.env['ir.config_parameter'].set_param(
            'agriculture.OrganicRice', self.OrganicRice)
        self.env['ir.config_parameter'].set_param(
            'agriculture.VolumeWeightIsOverAndEqualTo', self.VolumeWeightIsOverAndEqualTo)
        self.env['ir.config_parameter'].set_param(
            'agriculture.PrimeYieldIsOverAndEqualTo', self.PrimeYieldIsOverAndEqualTo)
        self.env['ir.config_parameter'].set_param(
            'agriculture.OrganicRiceExtra', self.OrganicRiceExtra)
        self.env['ir.config_parameter'].set_param(
            'agriculture.OrganicTransOrIso', self.OrganicTransOrIso)
        self.env['ir.config_parameter'].set_param(
            'agriculture.fs_VolumeWeightIsOver', self.fs_VolumeWeightIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.fs_TasteRatingIsOver', self.fs_TasteRatingIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.fs_BrownIntactRatioIsOver', self.fs_BrownIntactRatioIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.fs_bonus', self.fs_bonus)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ss_VolumeWeightIsOver', self.ss_VolumeWeightIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ss_TasteRatingIsOver', self.ss_TasteRatingIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ss_BrownIntactRatioIsOver', self.ss_BrownIntactRatioIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ss_bonus', self.ss_bonus)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ts_VolumeWeightIsOver', self.ts_VolumeWeightIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ts_TasteRatingIsOver', self.ts_TasteRatingIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ts_BrownIntactRatioIsOver', self.ts_BrownIntactRatioIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ts_bonus', self.ts_bonus)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ffs_VolumeWeightIsOver', self.ffs_VolumeWeightIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ffs_TasteRatingIsOver', self.ffs_TasteRatingIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.ffs_BrownIntactRatioIsOver', self.ffs_BrownIntactRatioIsOver)
        self.env['ir.config_parameter'].set_param(
            'agriculture.tgap_bonus', self.tgap_bonus)
        self.env['ir.config_parameter'].set_param(
            'agriculture.final_PrimeYieldIsOverAndEqualTo', self.final_PrimeYieldIsOverAndEqualTo)
        self.env['ir.config_parameter'].set_param(
            'agriculture.multiplication', self.multiplication)

        return res

    def get_values(self):
        """agriculture limit getting field values"""
        res = super(Preferences, self).get_values()
        value_BasePrice = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.BasePrice', default=1400.0)
        value_ContractedMemberPrice = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ContractedMemberPrice', default=150.0)
        value_KoshihikariRice = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.KoshihikariRice', default=1050.0)
        value_GlutinousRicePrice_BR = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.GlutinousRicePrice_BR', default=850.0)
        value_GlutinousRicePrice = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.GlutinousRicePrice', default=150.0)
        value_OrganicRice = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.OrganicRice', default=750.0)
        value_VolumeWeightIsOverAndEqualTo = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.VolumeWeightIsOverAndEqualTo', default=610.0)
        value_PrimeYieldIsOverAndEqualTo = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.PrimeYieldIsOverAndEqualTo', default=70)
        value_OrganicRiceExtra = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.OrganicRiceExtra', default=300.0)
        value_OrganicTransOrIso = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.OrganicTransOrIso', default=650.0)
        value_fs_VolumeWeightIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.fs_VolumeWeightIsOver', default=610.0)
        value_fs_TasteRatingIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.fs_TasteRatingIsOver', default=73)
        value_fs_BrownIntactRatioIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.fs_BrownIntactRatioIsOver', default=80)
        value_fs_bonus = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.fs_bonus', default=180.0)
        value_ss_VolumeWeightIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ss_VolumeWeightIsOver', default=590.0)
        value_ss_TasteRatingIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ss_TasteRatingIsOver', default=65)
        value_ss_BrownIntactRatioIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ss_BrownIntactRatioIsOver', default=70)
        value_ss_bonus = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ss_bonus', default=120.0)
        value_ts_VolumeWeightIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ts_VolumeWeightIsOver', default=560.0)
        value_ts_TasteRatingIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ts_TasteRatingIsOver', default=64)
        value_ts_BrownIntactRatioIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ts_BrownIntactRatioIsOver', default=65)
        value_ts_bonus = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ts_bonus', default=60.0)
        value_ffs_VolumeWeightIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ffs_VolumeWeightIsOver', default=539.0)
        value_ffs_TasteRatingIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ffs_TasteRatingIsOver', default=59)
        value_ffs_BrownIntactRatioIsOver = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.ffs_BrownIntactRatioIsOver', default=60)
        value_tgap_bonus = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.tgap_bonus', default=100.0)
        value_final_PrimeYieldIsOverAndEqualTo = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.final_PrimeYieldIsOverAndEqualTo', default=63)
        value_multiplication = self.env['ir.config_parameter'].sudo(
        ).get_param('agriculture.multiplication', default=20.0)

        res.update(
            BasePrice=float(value_BasePrice),
            ContractedMemberPrice=float(value_ContractedMemberPrice),
            KoshihikariRice=float(value_KoshihikariRice),
            GlutinousRicePrice_BR=float(value_GlutinousRicePrice_BR),
            GlutinousRicePrice=float(value_GlutinousRicePrice),
            OrganicRice=float(value_OrganicRice),
            VolumeWeightIsOverAndEqualTo=float(
                value_VolumeWeightIsOverAndEqualTo),
            PrimeYieldIsOverAndEqualTo=float(value_PrimeYieldIsOverAndEqualTo),
            OrganicRiceExtra=float(value_OrganicRiceExtra),
            OrganicTransOrIso=float(value_OrganicTransOrIso),
            fs_VolumeWeightIsOver=float(value_fs_VolumeWeightIsOver),
            fs_TasteRatingIsOver=float(value_fs_TasteRatingIsOver),
            fs_BrownIntactRatioIsOver=float(value_fs_BrownIntactRatioIsOver),
            fs_bonus=float(value_fs_bonus),
            ss_VolumeWeightIsOver=float(value_ss_VolumeWeightIsOver),
            ss_TasteRatingIsOver=float(value_ss_TasteRatingIsOver),
            ss_BrownIntactRatioIsOver=float(value_ss_BrownIntactRatioIsOver),
            ss_bonus=float(value_ss_bonus),
            ts_VolumeWeightIsOver=float(value_ts_VolumeWeightIsOver),
            ts_TasteRatingIsOver=float(value_ts_TasteRatingIsOver),
            ts_BrownIntactRatioIsOver=float(value_ts_BrownIntactRatioIsOver),
            ts_bonus=float(value_ts_bonus),
            ffs_VolumeWeightIsOver=float(value_ffs_VolumeWeightIsOver),
            ffs_TasteRatingIsOver=float(value_ffs_TasteRatingIsOver),
            ffs_BrownIntactRatioIsOver=float(value_ffs_BrownIntactRatioIsOver),
            tgap_bonus=float(value_tgap_bonus),
            final_PrimeYieldIsOverAndEqualTo=float(
                value_final_PrimeYieldIsOverAndEqualTo),
            multiplication=float(value_multiplication)
        )
        return res
