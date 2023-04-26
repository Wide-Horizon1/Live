from odoo import fields, models


class ResPartnerNasr(models.Model):
    _inherit = 'res.partner'

    company_new_field = fields.Char(string="Company ID")
