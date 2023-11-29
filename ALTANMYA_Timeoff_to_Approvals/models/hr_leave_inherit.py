from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.http import request


class HrLeaveTypeInherit(models.Model):
    _inherit = "hr.leave"

    check_true = fields.Boolean(compute='check_if_true', store=True)

    state = fields.Selection(selection_add=[

        ('draft',),
        ('confirm',), ('refuse',),
        ('validate1',), ('validate',), ('submit', 'Submitted')

    ])
    created_from_calendar = fields.Boolean(string='Created From Calendar', default=False)

    def action_draft(self):
        if any(holiday.state not in ['confirm', 'refuse', 'submit'] for holiday in self):
            raise UserError(
                _('Time off request state must be "Refused" or "To Approve" in order to be reset to draft.'))
        self.write({
            'state': 'draft',
            'first_approver_id': False,
            'second_approver_id': False,
        })
        linked_requests = self.mapped('linked_request_ids')
        if linked_requests:
            linked_requests.action_draft()
            linked_requests.unlink()
        self.activity_update()

    def action_submit(self):
        for rec in self:
            period = dict(self._fields['request_date_from_period'].selection).get(self.request_date_from_period)
            hour_from = dict(self._fields['request_hour_from'].selection).get(self.request_hour_from)
            hour_to = dict(self._fields['request_hour_to'].selection).get(self.request_hour_to)
            to_mode = dict(self._fields['holiday_type'].selection).get(self.holiday_type)
            number_of_tickets_requested = self.number_of_ticket_allowance_ or 0
            approval_cat = self.env['approval.category'].search(
                [('id', '=', self.holiday_status_id.approval_type.id)])
            approval_request = {
                'category_id': rec.holiday_status_id.approval_id.id,
                'request_owner_id': rec.env.user.id,
                'name': rec.holiday_status_id.name,
                'parent_id': rec.id,
                'description': rec.name,
                'duration': rec.number_of_days_display,
                'employee_id': rec.employee_id.id,
                'half_day': rec.request_unit_half,
                'half_date': rec.request_date_from,
                'half_date_char': period,
                'custom_hours': rec.request_unit_hours,
                'hour_from': hour_from,
                'hour_to': hour_to,
                'hours_only': rec.number_of_hours_text,
                'main_date_from': rec.request_date_from,
                'main_date_to': rec.request_date_to,
                'mode': to_mode,
                'number_of_tickets_': number_of_tickets_requested,
                'attachment': [(6, 0, [rec.supported_attachment_ids.id])] if rec.supported_attachment_ids else False
            }
            if self.check_true == True:
                approval_request_vals = self.env['approval.request'].create(approval_request)
                approval_request_vals.action_confirm()
                rec.state = 'submit'
            elif rec.check_true == True and rec.check_true_for_ticket == True:
                approval_request_vals = self.env['approval.request'].create(approval_request)
                approval_request_vals.action_confirm()
                rec.state = 'submit'

    @api.depends('holiday_status_id')
    def check_if_true(self):
        for rec in self:
            c_true = self.env['hr.leave.type'].search([('leave_validation_type', '=', 'new')])
            if rec.holiday_status_id in c_true:
                rec.check_true = True
                print("recccc", rec.state)
                rec.state = 'draft'
            else:
                rec.check_true = False

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrLeaveTypeInherit, self).create(vals_list)
        for rec in res:
            print("dssadasdasdasdasdasdad",self._context.get('default_created_from_calendar'))
            if self._context.get('default_created_from_calendar') == True:
                print('sho ma kan', rec.number_of_ticket_allowance_)
                number_of_tickets_requested = rec.number_of_ticket_allowance_ or 0
                period = dict(rec._fields['request_date_from_period'].selection).get(rec.request_date_from_period)
                hour_from = dict(rec._fields['request_hour_from'].selection).get(rec.request_hour_from)
                hour_to = dict(rec._fields['request_hour_to'].selection).get(rec.request_hour_to)
                to_mode = dict(rec._fields['holiday_type'].selection).get(rec.holiday_type)
                approval_cat = self.env['approval.category'].search(
                    [('id', '=', rec.holiday_status_id.approval_type.id)])
                approval_request = {
                    'category_id': rec.holiday_status_id.approval_id.id,
                    'request_owner_id': rec.env.user.id,
                    'name': rec.holiday_status_id.name,
                    'parent_id': rec.id,
                    'description': rec.name,
                    'duration': rec.number_of_days_display,
                    'employee_id': rec.employee_id.id,
                    'half_day': rec.request_unit_half,
                    'half_date': rec.request_date_from,
                    'half_date_char': period,
                    'custom_hours': rec.request_unit_hours,
                    'hour_from': hour_from,
                    'hour_to': hour_to,
                    'hours_only': rec.number_of_hours_text,
                    'main_date_from': rec.request_date_from,
                    'main_date_to': rec.request_date_to,
                    'mode': to_mode,
                    'number_of_tickets_': number_of_tickets_requested,
                    'attachment': [(6, 0, [rec.supported_attachment_ids.id])] if rec.supported_attachment_ids else False
                }
                if rec.check_true:
                    approval_request_vals = rec.env['approval.request'].create(approval_request)
                    approval_request_vals.action_confirm()
                    rec.state = 'submit'
                elif  rec.check_true == True and rec.check_true_for_ticket ==True :
                    approval_request_vals = rec.env['approval.request'].create(approval_request)
                    approval_request_vals.action_confirm()
                    rec.state = 'submit'
            else:
               return res
            # approval_cat = self.env['approval.category'].search(
            #     [('id', '=', rec.holiday_status_id.approval_type.id)])
            # number_of_tickets_requested = rec.number_of_ticket_allowance_ or 0
            # period = dict(rec._fields['request_date_from_period'].selection).get(rec.request_date_from_period)
            # hour_from = dict(rec._fields['request_hour_from'].selection).get(rec.request_hour_from)
            # hour_to = dict(rec._fields['request_hour_to'].selection).get(rec.request_hour_to)
            # to_mode = dict(rec._fields['holiday_type'].selection).get(rec.holiday_type)
            # if rec.check_true_for_ticket == True and rec.check_true == False:
            #     approval_req = {
            #         'category_id': approval_cat.id,
            #         'request_owner_id': rec.env.user.id,
            #         'name': rec.holiday_status_id.name,
            #         'parent_id': rec.id,
            #         'description': rec.name,
            #         'duration': rec.number_of_days_display,
            #         'employee_id': rec.employee_id.id,
            #         'half_day': rec.request_unit_half,
            #         'half_date': rec.request_date_from,
            #         'half_date_char': period,
            #         'custom_hours': rec.request_unit_hours,
            #         'hour_from': hour_from,
            #         'hour_to': hour_to,
            #         'hours_only': rec.number_of_hours_text,
            #         'main_date_from': rec.request_date_from,
            #         'main_date_to': rec.request_date_to,
            #         'mode': to_mode,
            #         'number_of_tickets_': number_of_tickets_requested,
            #         'attachment': [(6, 0, [rec.supported_attachment_ids.id])] if rec.supported_attachment_ids else False
            #     }
            #     approval_request_vals = self.env['approval.request'].create(approval_req)
            #     approval_request_vals.action_confirm()
        return res
