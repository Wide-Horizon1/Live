from odoo import api, fields, models, tools
from datetime import datetime

class tanEmpAllocation(models.Model):
    _name = 'emp.allocation.public.holiday'
    _description = 'Allocation for public holiday'
    employee_id= fields.Many2one('hr.employee',string='Employee name', readonly=True, ondelete='cascade')
    allocation_id = fields.Many2one('hr.leave.allocation', string='Employee name', readonly=True, ondelete='cascade')
