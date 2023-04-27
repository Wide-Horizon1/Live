from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ShiftProductionNasr(models.Model):
    _name = 'shift.production'
    _rec_name = 'sequence'
    _description = 'Shift Production'

    sequence = fields.Char(required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    shift = fields.Many2one('resource.calendar', string="Shift")
    job_ticket = fields.Many2one('mrp.production', string="Job Ticket")
    finished_product = fields.Many2one('product.product', string="Finished Product",
                                       compute="_compute_finished_product")
    operation = fields.Many2one('mrp.routing.workcenter', string="Operation")
    operator = fields.Many2one('hr.employee', string="Operator")
    date = fields.Datetime(string='Date')
    duration_from = fields.Float(string='Duration From')
    duration_to = fields.Float(string='Duration To')
    quantity_done = fields.Float(string='Quantity Done')
    duration = fields.Float(string='Duration', compute="_compute_duration")
    outs = fields.Float(string='Outs')
    sheets_done = fields.Float(string='Sheets Done')
    job_ticket_qty = fields.Float(string='Sheets Done', compute="_compute_job_ticket_qty")

    @api.onchange('sheets_done', 'outs')
    def compute_quantity_done(self):
        for rec in self:
            rec.quantity_done = rec.sheets_done * rec.outs

    @api.depends('job_ticket')
    def _compute_job_ticket_qty(self):
        for rec in self:
            if rec.job_ticket:
                rec.job_ticket_qty = rec.job_ticket.product_qty
            else:
                rec.job_ticket_qty = None

    @api.onchange('job_ticket')
    def set_domain_for_product(self):
        for rec in self:
            res = {}
            res['domain'] = {'operation': [('id', 'in', rec.job_ticket.workorder_ids.workcenter_id.ids)]}
            return res

    @api.onchange('quantity_done', 'outs')
    def compute_sheets_done(self):
        for rec in self:
            if rec.outs == 0:
                rec.sheets_done = 0
            else:
                rec.sheets_done = rec.quantity_done / rec.outs

    @api.constrains('quantity_done')
    def check_quantity_done(self):
        for rec in self:
            if rec.quantity_done > rec.job_ticket_qty:
                raise ValidationError(
                    _('Quantity of shift production must be equal or less than the quantity of manufacturing order'))
            else:
                all_shifts = rec.env['shift.production'].search([('job_ticket', 'in', rec.job_ticket.ids)])
                qty = rec.quantity_done
                for lines in all_shifts:
                    if rec.operation == lines.operation and rec.id != lines.id:
                        qty = qty + lines.quantity_done
                        if qty > rec.job_ticket_qty:
                            raise ValidationError(
                                _('Total of quantities of shift production from the same operation must be equal or less than the quantity of manufacturing order'))

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == ('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('shift.production') or _('New')
        return super(ShiftProductionNasr, self).create(vals)

    @api.onchange('finished_product')
    def compute_outs(self):
        for rec in self:
            # if rec.outs is None:
            product = rec.env['product.template'].search([('id', '=', rec.finished_product.id)])
            rec.outs = product.outs

    @api.depends('job_ticket')
    def _compute_finished_product(self):
        for rec in self:
            if rec.job_ticket:
                rec.finished_product = rec.job_ticket.product_id
            else:
                rec.finished_product = None

    def _compute_duration(self):
        for rec in self:
            rec.duration = rec.duration_to - rec.duration_from
