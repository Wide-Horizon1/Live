from odoo import api, fields, models, tools
from datetime import datetime

class tanPublicHoliday(models.Model):
    _inherit = 'resource.calendar.leaves'
    @api.model
    def create(self, vals_list):
            emp_recs = []
            emps = self.env['hr.employee'].search([('active', '=', 'true')])
            for rec in emps:
                unusaldays = rec._get_unusual_days(vals_list['date_from'],vals_list['date_to'])
                if unusaldays and len([elem for elem in unusaldays.values() if elem]) > 0:
                    print('unusual day from emp: ' + rec.name + ' in date: ')
                    print(unusaldays)
                    emp_recs.append(rec.id)
            cod_holiday = self.env['hr.leave.type'].sudo().search([('name', '=', 'Compensatory Days for public')], limit=1)
            res = super(tanPublicHoliday, self).create(vals_list)
            if res:
                if len(emp_recs )>0:
                    all_rec = self.env['hr.leave.allocation'].sudo().create({
                        'name': 'allocation ' + str(rec.id),
                        'holiday_status_id': cod_holiday.id,
                        'allocation_type': 'regular',
                        'date_from': res.date_from,
                        'number_of_days': 1,
                        'holiday_type': 'employee',
                        'multi_employee':True,
                        'employee_ids': emp_recs,

                    })
                    all_rec.action_confirm()
                    for ee in emp_recs:
                        self.env['emp.allocation.public.holiday'].sudo().create(
                            {
                                "employee_id": ee,
                                "allocation_id": all_rec.id,
                            }
                    )
            return res





