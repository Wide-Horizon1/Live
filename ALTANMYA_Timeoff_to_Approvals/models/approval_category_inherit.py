from odoo import api, fields, models, _


class ApprovalCategoryInherit(models.Model):
    _inherit = "approval.category"

    time_off = fields.Boolean(string='Time Off')
    for_day = fields.Boolean(string='for day', compute='_method_for_day', default=False)
    for_half_day = fields.Boolean(string='for half day', compute='_method_for_half_day', default=False)
    for_hours = fields.Boolean(string='for hours', compute='_method_for_hours', default=False)
    has_period = fields.Selection(compute='_customize_settings', readonly=False, store=True)

    @api.depends('name')
    def _method_for_half_day(self):
        for record in self:
            half = self.env['hr.leave.type'].search([('leave_validation_type', '=', 'new'),('approval_id', '=', self.name),('request_unit', '=', 'half_day')])
            if half:
                record.for_half_day = True
            else:
                record.for_half_day = False

    @api.depends('name')
    def _method_for_hours(self):
        for record in self:
            hour = self.env['hr.leave.type'].search(
                [('leave_validation_type', '=', 'new'), ('approval_id', '=', self.name),
                 ('request_unit', '=', 'hour')])
            if hour:
                record.for_hours = True
            else:
                record.for_hours = False

    @api.depends('name')
    def _method_for_day(self):
        for record in self:
            hour = self.env['hr.leave.type'].search(
                [('leave_validation_type', '=', 'new'), ('approval_id', '=', self.name),
                 ('request_unit', '=', 'day')])
            if hour:
                record.for_day = True
            else:
                record.for_day = False
