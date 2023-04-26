from odoo import fields, models


class SaleOrderNasr(models.Model):
    _inherit = 'sale.order'

    to_ID = fields.Many2one('res.partner', string="To")
    received_on = fields.Datetime(string="Received on")
    p_o = fields.Datetime(string="Dated")
