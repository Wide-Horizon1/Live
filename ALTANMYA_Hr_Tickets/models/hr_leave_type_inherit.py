from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class HrLeaveTypeInherit(models.Model):
    _inherit = "hr.leave.type"

    ticket_allowance = fields.Boolean(string='Ticket Allowance')
    approval_type = fields.Many2one('approval.category', string='Approval Type')


class HrLeaveInherit(models.Model):
    _inherit = "hr.leave"

    ticket_allowance_ = fields.Boolean(string='Request for tickets')
    employee_id_ = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.user.employee_id.id)

    number_of_ticket_allowance_ = fields.Integer(string='Number of tickets')
    check_true_for_ticket = fields.Boolean(string='Request for tickets', compute='check_if_true_ticket')
    req_date = fields.Datetime(string='Date')
    state_of_req = fields.Selection([
        ('notapproved', 'not Approved'),
        ('approved', 'Done'),
    ], default='notapproved')
    parent_id = fields.Many2one('approval.request', string='Parent')

    @api.depends('holiday_status_id')
    def check_if_true_ticket(self):
        for rec in self:
            c_true = self.env['hr.leave.type'].search([('ticket_allowance', '=', True)])
            if rec.holiday_status_id in c_true:
                rec.check_true_for_ticket = True
            else:
                rec.check_true_for_ticket = False

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrLeaveInherit, self).create(vals_list)
        for values in vals_list:
            print("values is ", values)

            employee_id = values.get('employee_id')
            number_of_tickets_requested = values.get('number_of_ticket_allowance_', 0)
            nation = self.env['ticket.allowance.settings.lines'].search([])

            if number_of_tickets_requested < 0:
                raise ValidationError(_('You cannot request a negative number of tickets!'))

            employee = self.env['hr.employee'].browse(employee_id)
            if number_of_tickets_requested > employee.number_of_tickets_start_end:
                raise ValidationError(_(
                    'You cannot request tickets exceeding the number of tickets specified in your contract. '
                    'The number of tickets in your contract is (%s)' % employee.number_of_tickets_start_end
                ))

            if not employee.country_id:
                raise ValidationError(
                    _('Please specify your nationality first!'))

            found_matching_nationality = False

            for record in nation:
                if employee.country_id.name == record.nationality_id.name:
                    found_matching_nationality = True
                    break

            if not found_matching_nationality:
                raise ValidationError(_('There is no cost for your nationality!'))
        return res

    def action_approve(self):
        super(HrLeaveInherit, self).action_approve()
        # for rec in res:
        #     print("reeeeeeeeeeeeeees cat is ", rec.employee_id_)

        print("caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa cat is ", self.employee_id_)
        employees = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        for rec in self:
            employee_id = rec.employee_id
            number_of_tickets_requested = rec.number_of_ticket_allowance_ or 0
            approval_cat = rec.env['approval.category'].search([('id', '=', rec.holiday_status_id.approval_type.id)])
            name = rec.env['hr.leave.type'].browse(self.holiday_status_id.id)
            print("approval cat is ", approval_cat.name, rec.state_of_req, employee_id, self.employee_id_)
            rec.req_date = datetime.now()
            if approval_cat and rec.ticket_allowance_ :
                print("action approve from leave ##############", rec.check_true_for_ticket)
                approval_request = {
                    'number_of_tickets_': number_of_tickets_requested,
                    'category_id': approval_cat.id,
                    'request_owner_id': rec.env.user.id,
                    'name': name.name,
                    'employee_id': employee_id.id,
                    'check_from_leave': rec.check_true_for_ticket,
                    'req_date': rec.req_date,
                    'state_of_req_approval': 'approved',
                    'parent_id': rec.id,
                    'refuse_butt': True
                }
                approval_request_vals = rec.env['approval.request'].create(approval_request)
                approval_request_vals.action_confirm()
                print('approval request1111111111', approval_request_vals)

    # def action_refuse(self):
    #     super(HrLeaveInherit, self).action_refuse()
    #
    #     for rec in self:
    #         approval_request = rec.env['approval.request'].search(
    #             [('parent_id', '=', rec.id), ('state_of_req_approval', '=', 'approved'), ('refuse_butt', '=', True)], limit=1)
    #         if approval_request:
    #             approval_request.action_refuse()
