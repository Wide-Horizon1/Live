from odoo import models, api, fields, Command


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to', 'struct_id')
    def _compute_input_line_ids(self):
        attachment_types = self._get_attachment_types()
        attachment_type_ids = [f.id for f in attachment_types.values()]
        for slip in self:
            if not slip.employee_id or not slip.employee_id.salary_attachment_ids or not slip.struct_id:
                lines_to_remove = slip.input_line_ids.filtered(lambda x: x.input_type_id.id in attachment_type_ids)
                slip.update({'input_line_ids': [Command.unlink(line.id) for line in lines_to_remove]})
            if slip.employee_id.salary_attachment_ids:
                lines_to_remove = slip.input_line_ids.filtered(lambda x: x.input_type_id.id in attachment_type_ids)
                input_line_vals = [Command.unlink(line.id) for line in lines_to_remove]

                valid_attachments = slip.employee_id.salary_attachment_ids.filtered(
                    lambda a: a.state == 'open' and a.date_start <= slip.date_to
                )

                # Only take deduction types present in structure
                print('valid_attachments : ', valid_attachments, attachment_types)
                deduction_types = list(set(valid_attachments.mapped('deduction_type')))
                struct_deduction_lines = list(set(slip.struct_id.rule_ids.mapped('code')))
                print('ll', deduction_types)
                included_deduction_types = [f for f in deduction_types if
                                            attachment_types[str(f.name)].code in struct_deduction_lines]
                for deduction_type in included_deduction_types:
                    if not slip.struct_id.rule_ids.filtered(
                            lambda r: r.active and r.code == attachment_types[deduction_type.name].code):
                        continue
                    attachments = valid_attachments.filtered(lambda a: a.deduction_type == deduction_type)
                    amount = sum(attachments.mapped('active_amount'))
                    name = ', '.join(attachments.mapped('description'))
                    input_type_id = attachment_types[deduction_type.name].id
                    input_line_vals.append(Command.create({
                        'name': name,
                        'amount': amount,
                        'input_type_id': input_type_id,
                    }))
                slip.update({'input_line_ids': input_line_vals})

    @api.model
    def _get_attachment_types(self):
        attachment_types = self.env['hr.payslip.input.type'].search([])
        print('attachment types ', attachment_types)
        att_types = dict()
        for attachment_type in attachment_types:
            att_types[attachment_type.name] = attachment_type
        print(att_types)
        return att_types
        # return {
        #     'attachment': self.env.ref('hr_payroll.input_attachment_salary'),
        #     'assignment': self.env.ref('hr_payroll.input_assignment_salary'),
        #     'child_support': self.env.ref('hr_payroll.input_child_support'),
        # }
