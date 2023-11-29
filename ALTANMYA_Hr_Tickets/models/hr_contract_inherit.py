from odoo import api, fields, models


class HrContractInherit(models.Model):
    _inherit = "hr.contract"

    contract_tickets = fields.Integer(string="Number of tickets")