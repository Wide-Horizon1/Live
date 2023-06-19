from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    employee_sequence_registration_number = fields.Integer(string="Department Registration Sequence")
