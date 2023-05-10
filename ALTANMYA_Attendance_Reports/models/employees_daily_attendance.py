from odoo import api, fields, models, tools


class EmployeeAttendanceReport(models.Model):
    _name = "employees.daily.attendance.report"

    employee_id = fields.Integer(string='رقم الموظف')
    employee_name = fields.Char(string='اسم الموظف')
    department_name = fields.Char(string='اسم القسم')
    day_type = fields.Char(string='وضع اليوم')
    date = fields.Date(string='التاريخ')
    sign_in1 = fields.Datetime(string='ساعة الدخول')
    sign_out1 = fields.Datetime(string='ساعة الخروج')
    hourly_leave = fields.Integer(string='مدة الساعية')
    work_hours = fields.Char(string='نوع الساعية')
    late_entry = fields.Integer(string='مدة التأخر')

    def open_choose_date_total_att_wizard(self):
        """ Creates a new export wizard for this report and returns an act_window
        opening it. A new account_report_generation_options key is also added to
        the context, containing the current options selected on this report
        """
        new_wizard = self.env['emp.total.att.wizard'].create({})
        view_id = self.env.ref('ALTANMYA_Attendance_Reports.choose_employees_total_attendance').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Choose Date',
            'view_mode': 'form',
            'res_model': 'emp.total.att.wizard',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    def open_choose_date_wizard(self):
        """ Creates a new export wizard for this report and returns an act_window
        opening it. A new account_report_generation_options key is also added to
        the context, containing the current options selected on this report
        """
        new_wizard = self.env['emp.daily.att.wizard'].create({})
        view_id = self.env.ref('ALTANMYA_Attendance_Reports.choose_employee_daily_attendance').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Choose Date',
            'view_mode': 'form',
            'res_model': 'emp.daily.att.wizard',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    def open_choose_employee_wizard(self):
        """ Creates a new export wizard for this report and returns an act_window
        opening it. A new account_report_generation_options key is also added to
        the context, containing the current options selected on this report
        """
        new_wizard = self.env['emp.monthly.att.wizard'].create({})
        view_id = self.env.ref('ALTANMYA_Attendance_Reports.choose_employee_monthly_attendance').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Choose Employee',
            'view_mode': 'form',
            'res_model': 'emp.monthly.att.wizard',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }
