# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        temp_employee = self.env['hr.employee'].search([('id', '>', -1)])
        for temp_emp in temp_employee:
            if temp_emp.name.isdigit():
                temp_emp.unlink()
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)


