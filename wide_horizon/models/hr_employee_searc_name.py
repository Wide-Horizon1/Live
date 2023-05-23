from odoo import models, api


class HrEmployeeCSV(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        domain = []
        if args is None:
            args = []
        if name:
            domain = ['|', ('name', 'ilike', name), ('registration_number', '=', name)]
            if args:
                domain += args
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + str(rec.registration_number) + '] ' + rec.name
            result.append((rec.id, name))
        return result

    @api.model
    def create(self, vals):
        if vals['department_id']:
            department = self.env['hr.employee'].search([('department_id', '=', vals['department_id']), '|', ('active', '=', True),  ('active', '=', False)])
            # print('department', department)
            if not department:
                # print('1', department)
                vals['registration_number'] = self.env['hr.department'].search([('id', '=', vals['department_id'])]).employee_sequence_registration_number + 1
            else:
                # print('2', department[0].department_id.name, department[0].department_id)
                vals['registration_number'] = department[0].department_id.employee_sequence_registration_number + len(department) + 1

        return super(HrEmployeeCSV, self).create(vals)
