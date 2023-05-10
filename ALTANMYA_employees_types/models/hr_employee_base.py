from odoo import models, fields


class HrEmployeeBase(models.AbstractModel):
    _inherit = ["hr.employee.base"]
    # employee_type = fields.Selection([
    #     ('employee', 'Employee'),
    #     ('student', 'Student'),
    #     ('trainee', 'Trainee'),
    #     ('contractor', 'Contractor'),
    #     ('freelance', 'Freelancer'),
    # ], string='Employee Type', default='employee', required=True,
    #     help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")
    employee_type = fields.Selection([
        ('employee', 'عامل'),
        # ('leader', 'قيادي'),
        ('student', 'طالب'),
        ('trainee', 'قيادي'),
        ('contractor', 'متعاقد'),
        ('freelance', 'عمل حر'),
    ], string='Employee Type', default='employee', required=True,
        help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")

    # def action_open_contract_leader_history(self):
    #     self.ensure_one()
    #     action = self.env["ir.actions.actions"]._for_xml_id('ALTANMYA_employees_types.hr_contract_history_view_leader_form_action')
    #     action['res_id'] = self.id
    #     return action