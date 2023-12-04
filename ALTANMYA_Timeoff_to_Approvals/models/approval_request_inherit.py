from odoo import api, fields, models


class HrLeaveTypeInherit(models.Model):
    _inherit = "approval.request"

    parent_id = fields.Many2one('hr.leave', string='Parent')
    description = fields.Char(string='Description', readonly=True)
    duration = fields.Float(string='Duration', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    mode = fields.Char(string='Mode', readonly=True)
    half_date = fields.Date(string='Date', readonly=True)
    half_date_char = fields.Char(string='', readonly=True)
    check_timeoff = fields.Boolean(string='Check Timeoff', compute='check_if_true', readonly=True)
    check_day = fields.Boolean(string='Check Day', compute='check_if_day', readonly=True)
    check_halfday = fields.Boolean(string='Check Half', compute='check_if_half', readonly=True)
    check_hours = fields.Boolean(string='Check Hours', compute='check_if_hours', readonly=True)
    half_day = fields.Boolean(string='Half Day', readonly=True)
    custom_hours = fields.Boolean(string='Custom Hours', readonly=True)
    hour_from = fields.Char(string='', readonly=True)
    hour_to = fields.Char(string='', readonly=True)
    hours_only = fields.Char(string='', readonly=True)
    main_date_from = fields.Date(string='', readonly=True)
    main_date_to = fields.Date(string='', readonly=True)
    attachment = fields.Many2many('ir.attachment', string='Supporting Document', readonly=True)

    def _compute_request_status(self):
        super(HrLeaveTypeInherit, self)._compute_request_status()
        for rec in self:
            print("iiiiiiiiiiiiiiiii")
            if rec.request_status == 'approved':
                leave_ids = self.env['hr.leave'].search([('id', '=', rec.parent_id.id)])
                leave_ids.action_draft()
                leave_ids.action_confirm()
                leave_ids.action_approve()
                print("rrrrrrrrrrrrrrrrrrrrrrrrrr")

    def action_refuse(self, approver=None):
        super(HrLeaveTypeInherit, self).action_refuse()
        for rec in self:
            leave_ids = self.env['hr.leave'].search([('id', '=', rec.parent_id.id)])
            leave_ids.action_draft()
            leave_ids.action_confirm()
            leave_ids.action_refuse()

    def action_withdraw(self, approver=None):
        for rec in self:
            leave_ids = self.env['hr.leave'].search([('id', '=', rec.parent_id.id)])
            if leave_ids.state == 'refuse':
                leave_ids.action_draft()
                leave_ids.action_confirm()
            leave_ids.action_refuse()
            leave_ids.action_draft()
            leave_ids.action_confirm()
        super(HrLeaveTypeInherit, self).action_withdraw()

    @api.depends('category_id.time_off')
    def check_if_true(self):
        for rec in self:
            rec.check_timeoff = rec.category_id.time_off

    @api.depends('category_id.for_half_day')
    def check_if_half(self):
        for rec in self:
            rec.check_halfday = rec.category_id.for_half_day

    @api.depends('category_id.for_hours')
    def check_if_hours(self):
        for rec in self:
            rec.check_hours = rec.category_id.for_hours

    @api.depends('category_id.for_day')
    def check_if_day(self):
        for rec in self:
            rec.check_day = rec.category_id.for_day

