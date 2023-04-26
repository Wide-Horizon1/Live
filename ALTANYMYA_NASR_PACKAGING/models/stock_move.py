from datetime import datetime, timedelta

from odoo import api, fields, models


class StockMoveNasr(models.Model):
    _inherit = 'stock.move'

    delivery_date_per_item = fields.Datetime("Delivery Date", compute="_compute_delivery_date_per_item")
    lead_days = fields.Integer(string="Lead Days", compute="_compute_lead_days")

    @api.depends('product_id')
    def _compute_lead_days(self):
        for rec in self:
            if rec.product_id.sale_delay:
                rec.lead_days = rec.product_id.sale_delay
            elif rec.company_id.security_lead and not rec.product_id.sale_delay:
                rec.lead_days = rec.company_id.security_lead
            else:
                rec.lead_days = 0

    @api.depends('picking_id', 'location_dest_id')
    def _compute_delivery_date_per_item(self):
        for rec in self:
            if rec.location_dest_id.usage == 'customer':
                if rec.picking_id:
                    if rec.picking_id.sale_order_id:
                        values = self.env['sale.order.line'].search(
                            [('order_id', '=', rec.picking_id.sale_order_id.ids)])
                        for lines in values:
                            if lines.product_id == rec.product_id:
                                del_date = lines.delivery_date_sale_order_line
                                if del_date:
                                    old_date = datetime.strptime(str(del_date), '%Y-%m-%d %H:%M:%S')
                                    new_date = old_date - timedelta(days=rec.lead_days)
                                    rec.delivery_date_per_item = new_date.strftime('%Y-%m-%d %H:%M:%S')
                                else:
                                    rec.delivery_date_per_item = None
                    else:
                        rec.delivery_date_per_item = None
                else:
                    rec.delivery_date_per_item = None
            elif rec.location_dest_id.usage == 'internal':
                if rec.origin:
                    manufacture_order = rec.env['mrp.production'].search([('name', '=', rec.origin)])
                    if manufacture_order.name == rec.origin:
                        for order in manufacture_order:
                            rec.delivery_date_per_item = order.schedule_date_mrp
                    else:
                        # todo
                        if rec.picking_id.state == 'done':
                            rec.delivery_date_per_item = rec.picking_id.delivery_date_per_item_done
                        else:
                            rec.delivery_date_per_item = None
                else:
                    rec.delivery_date_per_item = None
            else:
                rec.delivery_date_per_item = None
