from odoo import models, fields, api


class HrAttendanceCSV(models.Model):
    _inherit = 'hr.attendance'
    reg_number = fields.Char(string="Registration Number")
    emp = fields.Char(string="Employee", compute="_compute_emp")
    del_emp = fields.Char(string="Employee", compute="_compute_del_emp")

    @api.depends('employee_id')
    def _compute_del_emp(self):
        for rec in self:
            rec.del_emp = None

    @api.onchange('employee_id')
    def _compute_emp(self):
        for rec in self:
            rec.emp = rec.reg_number
            rec.reg_number = rec.employee_id.registration_number

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        temp_attendance = self.env['hr.attendance'].search([('id', '>', -1)])
        for rec in temp_attendance:
            if rec.emp:
                rec.employee_id = self.env['hr.employee'].search([('registration_number', '=', rec.emp)])
        return res


class HrEmployeeCSV(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        temp_employee = self.env['hr.employee'].search([('id', '>', -1)])
        for temp_emp in temp_employee:
            if temp_emp.name.isdigit():
                temp_emp.unlink()
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + str(rec.registration_number) + '] ' + rec.name
            result.append((rec.id, name))
        return result
