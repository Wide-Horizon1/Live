from time import strptime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class ApprovalCategoryInherit(models.Model):
    _inherit = 'approval.category'

    allowance_tickets = fields.Boolean(string='Ticket Allowance?')

    @api.onchange('allowance_tickets', 'time_off')
    def onchange_customize_settings(self):
        fields_to_update = ['has_period', 'requirer_document', 'has_partner', 'has_date', 'has_product', 'has_quantity',
                            'has_amount', 'has_reference', 'has_payment_method', 'has_location']

        for field_name in fields_to_update:
            field_value = getattr(self, field_name)
            if field_value == 'required':
                setattr(self, field_name, 'optional')


class ApprovalRequestInherit(models.Model):
    _inherit = 'approval.request'

    number_of_tickets_ = fields.Integer(string='Number of tickets')
    approved_tickets_ = fields.Integer(string='Approved tickets')
    tick_category = fields.Boolean(related='category_id.allowance_tickets')
    employee_id = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.user.employee_id.id)
    req_date = fields.Datetime(string='Date')
    check_from_leave = fields.Boolean()
    check_from_leave_copy = fields.Boolean()
    hide_butt = fields.Boolean(default=False)
    state_of_req_approval = fields.Char('')


    def _compute_request_status(self):
        super(ApprovalRequestInherit, self)._compute_request_status()
        employees = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        for rec in self:
            print('before$$$$$$$$', self.check_from_leave)
            rec.check_from_leave_copy = self.check_from_leave
            if rec.request_status == 'approved':
                self.req_date = datetime.now()
                print('after%%%%%%%%%%', self.check_from_leave, self.state_of_req_approval)
                print("datttttttttte ============== ", self.req_date, rec.check_from_leave_copy)
                operations_lines = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
                approved_val = self.env['approval.request'].search(
                    [('request_status', '=', 'approved'), ('category_id.allowance_tickets', '=', True), ('state_of_req_approval', '=', 'approved')],
                    order="id desc", limit=1)
                ticket_cost = self.env['ticket.allowance.settings.lines'].search([('nationality_id', '=',
                                                                                   rec.employee_id.country_id.id)])


                for employee in employees:
                    print("start end ----------", employee.number_of_tickets_start_end, self.number_of_tickets_)
                    if self.number_of_tickets_ <= employee.number_of_tickets_start_end:
                        total = employee.number_of_tickets_start_end - self.number_of_tickets_
                        print('card value', employee.number_of_tickets_start_end)
                        print('tickets value', self.number_of_tickets_)
                        self.approved_tickets_ = total
                        print('my total', total)
                if employees.number_of_tickets_start_end < 0:
                    raise ValidationError(
                        _('The approval cannot be granted for the requested number of tickets, either because it exceeds the available number of tickets or because there are no more tickets left'))

                if rec.state_of_req_approval == 'approved':
                    print("خفففففففففففففففففف")
                    approval_type = rec.env['hr.payslip.input.type'].search([('name', '=', 'Ticket Allowance')])
                    monthly_settlements = {
                        'type': approval_type.id,
                        'employee_name': self.employee_id.id,
                        'num_of_tick': self.number_of_tickets_,
                        'date': self.req_date,
                        'state': 'done',
                        'date_time': self.req_date
                    }
                    self.hide_butt = True
                    print(self.hide_butt)
                    rec.env['monthly.settlements'].create(monthly_settlements)
                    for line in operations_lines:
                        line.write({'ticket_log_line_ids': [(0, 0,
                                                             {'requested_tickets_num': approved_val.number_of_tickets_,
                                                              'request_date': approved_val.req_date,
                                                              'cost_of_one_ticket': ticket_cost.cost,
                                                              'appr_req_id': rec.id})]})
                        print('dateeeeeeeeeee00000', rec.id)
            elif rec.request_status == 'refused':
                print('refuseeeeeeeeeeed', self.check_from_leave)
                if rec.state_of_req_approval == 'approved':
                    print('kiko')
                    approved_val = self.env['approval.request'].search(
                        [('request_status', '=', 'refused'), ('category_id.allowance_tickets', '=', True), ('state_of_req_approval', '=', 'approved')],
                        order="id desc", limit=1)
                    approval_type = self.env['hr.payslip.input.type'].search([('name', '=', 'Ticket Allowance')])
                    existing_settlement = self.env['monthly.settlements'].search([
                        ('type', '=', approval_type.id),
                        ('employee_name', '=', rec.employee_id.id),
                        ('num_of_tick', '=', rec.number_of_tickets_),
                        ('date', '=', rec.req_date),
                        ('state', '=', 'done'),
                        ('date_time', '=', rec.req_date)
                    ])
                    existing_settlement.unlink()
                    operations_lines = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
                    for line in operations_lines:
                        for v in line.ticket_log_line_ids:
                            print('heroooooooo', v.appr_req_id)
                            print('heroooooo222222',
                                  approved_val.id)

                        # print('heroooooooo', operations_lines,approved_val,approved_val.req_date)
                        created_line = line.ticket_log_line_ids.filtered(
                            lambda x: x.appr_req_id.id == approved_val.id)
                        print(created_line)
                        created_line.unlink()

    def action_confirm(self):

        for rec in self:
            nation = self.env['ticket.allowance.settings.lines'].search([])
            employees = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)], limit=1)
            for employee in employees:
                if self.number_of_tickets_ < 0:
                    raise ValidationError(
                        _('You cannot enter a negative number!'))

                if self.number_of_tickets_ > employee.number_of_tickets_start_end:
                    raise ValidationError(
                        _('You cannot request tickets exceeding the number of tickets specified in your contract. \nThe number of tickets in your contract is (%s) ',
                          employee.number_of_tickets_start_end))

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

            return super(ApprovalRequestInherit, self).action_confirm()

    def to_monthly_settlements(self):

        maria = {
            'name': 'Monthly Settlements',
            'type': 'ir.actions.act_window',
            'res_model': 'monthly.settlements',
            'view_mode': 'tree,form',
            'domain': [('date_time', '=', str(self.req_date))],

        }
        return maria


