from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderLineNasr(models.Model):
    _inherit = 'sale.order.line'
    job_type = fields.Selection([("repeat", "Repeat"), ("revised", "Revised"), ("new", "New")], default='new')
    delivery_date_sale_order_line = fields.Datetime(string="Delivery Date")
    manufacturing_order_id = fields.Many2one('mrp.production', string="MO ID", compute="_compute_manufacturing_order_id")
    finishing = fields.Char(string="Finishing")

    @api.depends('product_id', 'order_id')
    def _compute_manufacturing_order_id(self):
        for rec in self:
            rec.manufacturing_order_id = None
            if rec.product_id:
                if rec.order_id:
                    manufacturing_orders = rec.env['mrp.production'].search([('product_id', '=', rec.product_id.id)])
                    sale_order_id = rec.order_id
                    if manufacturing_orders and sale_order_id:
                        for i in manufacturing_orders:
                            if i.origin == sale_order_id.name:
                                rec.manufacturing_order_id = i
                    else:
                        rec.manufacturing_order_id = None
                else:
                    rec.manufacturing_order_id = None
            else:
                rec.manufacturing_order_id = None

    @api.constrains('delivery_date_sale_order_line')
    def check_delivery_date_sale_order_line(self):
        for rec in self:
            sale_order_id = self.env['sale.order'].search([('id', '=', rec.order_id.id)])
            if sale_order_id.commitment_date:
                if rec.delivery_date_sale_order_line >= sale_order_id.commitment_date:
                    raise ValidationError(
                        _('Delivery Date for each line must be less than the Sale Order Delivery Date'))
