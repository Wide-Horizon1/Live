from odoo import models, fields, api


class HrSalaryAttachment(models.Model):
    _inherit = 'hr.salary.attachment'
    _description = 'Salary Attachment'

    deduction_type = fields.Many2one(
        'hr.payslip.input.type',
        string='Type',
        required=True,
        tracking=True,
    )

    @api.depends('deduction_type', 'date_end')
    def _compute_has_total_amount(self):
        for record in self:
            if record.deduction_type.name == 'child_support' and not record.date_end:
                print('childs')
                record.has_total_amount = False
            else:
                record.has_total_amount = True
    # deduction_type_name = fields.Char('Deduction Type', related='deduction_type.name')

