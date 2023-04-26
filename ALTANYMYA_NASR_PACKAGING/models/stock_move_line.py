from odoo import api, fields, models


class StockMoveLineNasr(models.Model):
    _inherit = 'stock.move.line'

    pallet = fields.Integer(string="Pallet Number", default=1)
    delivery_date = fields.Datetime("Delivery Date", compute='_compute_delivery_date')

    @api.depends('move_id')
    def _compute_delivery_date(self):
        for rec in self:
            if rec.move_id:
                if rec.product_id == rec.move_id.product_id:
                    rec.delivery_date = rec.move_id.delivery_date_per_item
                else:
                    rec.delivery_date = None
            else:
                rec.delivery_date = None
