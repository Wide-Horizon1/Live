from odoo import api, fields, models, tools
from datetime import datetime, timedelta, date


class EmployeeAttendanceReport(models.Model):
    _name = "employee.attendance.report"

    employee_id = fields.Integer(string='رقم الموظف')
    employee_name = fields.Char(string='اسم الموظف')
    date = fields.Date(string='التاريخ')
    day_type = fields.Char(string='طبيعة اليوم')
    sign_in1 = fields.Datetime(string='دخول 1')
    sign_out1 = fields.Datetime(string='خروج 1')
    sign_in2 = fields.Datetime(string='دخول 2')
    sign_out2 = fields.Datetime(string='خروج 2')
    hourly_leave = fields.Char(string='إجازة ساعية')
    work_hours = fields.Integer(string='عدد ساعات العمل')
    late_entry = fields.Datetime(string='تأخر صباحي')
    early_out = fields.Datetime(string='خروج مبكر')

    def fetch_dates_between_2_dates(self):
        self._cr.execute("""SELECT date_trunc('day', dd):: date FROM generate_series
        ( '2023-03-01'::timestamp
        , '2023-03-31'::timestamp 
        , '1 day'::interval) dd
        """)
        return self._cr.fetchall()

    def fill_view_data(self):
        dates = self.fetch_dates_between_2_dates()
        print('dates ', dates)
        for date1 in dates:
            print('type', type(date1[0]), str(date1[0].strftime('%Y-%m-%d')))
            query = f"""SELECT he.name as emp_name,
                                hd.name as dep_name,
                                '' as entry1,
                                '' as out1,
                                '' as entry2,
                                '' as out2,
                                hwet.name as day_type,
                                oi.att_date,
                                oi.date_in, oi.date_out, hlt.name
                                from hr_work_entry hwe
                                LEFT JOIN hr_employee he on he.id = hwe.employee_id
                                LEFT JOIN hr_department hd ON hd.id = he.department_id
                                LEFT JOIN hr_work_entry_type hwet ON hwet.id = hwe.work_entry_type_id
                                LEFT JOIN od_inout oi ON oi.emp_deviceno = he.studio_employee_number
                                and oi.att_date = {(date1[0].isoformat())}
                                LEFT JOIN hr_leave hl ON hl.employee_id = he.id
                                and (hl.request_unit_half = TRUE OR hl.request_unit_hours = TRUE)
                                and hl.request_date_from = {(date1[0].isoformat())}
                                LEFT JOIN hr_leave_type hlt ON hlt.id = hl.holiday_status_id
								where {(date1[0].isoformat())} = Date(hwe.date_start)
								and hwe.employee_id = 1381
"""
            self._cr.execute(query)
            print('record : ', self._cr.fetchone())
            # SELECT he.name as emp_name,
            #                     hd.name as dep_name,
            #                     '' as entry1,
            #                     '' as out1,
            #                     '' as entry2,
            #                     '' as out2,
            #                     hwet.name as day_type,
            #                     oi.att_date,
            #                     oi.date_in, oi.date_out, hlt.name
            #                     LEFT JOIN hr_work_entry
            #                     hwe on {date1} = Date(hwe.date_start) and hwe.employee_id = 1381
            #                     LEFT JOIN hr_employee he on he.id = hwe.employee_id
            #                     LEFT JOIN hr_department hd ON hd.id = he.department_id
            #                     LEFT JOIN hr_work_entry_type hwet ON hwet.id = hwe.work_entry_type_id
            #                     LEFT JOIN od_inout oi ON oi.emp_deviceno = he.studio_employee_number
            #                     and oi.att_date = {date1}
            #                     LEFT JOIN hr_leave hl ON hl.employee_id = he.id
            #                     and (hl.request_unit_half = TRUE OR hl.request_unit_hours = TRUE)
            #                     and hl.request_date_from = {date1}
            #                     LEFT JOIN hr_leave_type hlt ON hlt.id = hl.holiday_status_id)

    # def init(self):
    #     self.fill_view_data()
        # tools.drop_view_if_exists(self._cr, 'employee_attendance_report')
        # self._cr.execute(""" CREATE VIEW employee_attendance_report AS (
        #     SELECT
        #     he.name as employee_name,
        #     he.id as employee_id,
        #     hd.name,
        #     hwe.date_start as date,
        #     hwet.name as day_type,
        #     from hr_employee he, hr_department hd, hr_work_entry
        #     hwe, hr_work_entry_type
        #     hwet
        #     WHERE
        #     he.id = hwe.employee_id and hwe.work_entry_type_id = hwet.id
        #     and he.department_id = hd.id
        #     and he.name = 'Eli Lambert'
        #     )
        #     """)
