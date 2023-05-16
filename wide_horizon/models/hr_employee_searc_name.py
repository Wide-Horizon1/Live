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
