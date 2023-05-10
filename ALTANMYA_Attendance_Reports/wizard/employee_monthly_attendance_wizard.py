from odoo import models, fields, api
from pytz import timezone, utc


class EmployeesAttendanceReportWizard(models.TransientModel):
    _name = 'emp.monthly.att.wizard'

    employee_name = fields.Many2one('hr.employee', string='اسم الموظف')
    start_date = fields.Date(string='تاريخ البداية')
    end_date = fields.Date(string='تاريخ النهاية')

    def fetch_dates_between_2_dates(self, start_date, end_date):
        print('start date ', start_date)
        print('end date ', end_date)
        self._cr.execute(f"""SELECT date_trunc('day', dd):: date FROM generate_series
                ( '{start_date.isoformat()}'::timestamp
                , '{end_date.isoformat()}'::timestamp 
                , '1 day'::interval) dd
                """)
        return self._cr.fetchall()

    def fill_view_data(self, employee_id, start_date, end_date):
        dates = self.fetch_dates_between_2_dates(start_date, end_date)
        print('dates ', dates)
        fetched_data = []
        for date1 in dates:
            print('dd', date1[0].isoformat())
            self.env.cr.execute(f"""
                                           select DISTINCT edl.log_date from emp_date_log edl, od_inout oi, hr_employee he
                                           where log_date::date = '{date1[0].isoformat()}'
                                           and oi.id = edl.inout_id
                                           and he.studio_employee_number = oi.emp_deviceno
                                           and he.id = {employee_id.id}
            """)
            logs = self.env.cr.fetchall()
            print('logs ', logs)
            print('type', type(date1[0]), str(date1[0].strftime('%Y-%m-%d')))
            log_1 = f'{logs[0][0].astimezone(timezone("Asia/baghdad")).strftime("%p %I:%M")}' if len(logs) >= 1 else ''
            log_2 = f'{logs[1][0].astimezone(timezone("Asia/baghdad")).strftime("%p %I:%M")}' if len(logs) >= 2 else ''
            log_3 = f'{logs[2][0].astimezone(timezone("Asia/baghdad")).strftime("%p %I:%M")}' if len(logs) >= 3 else ''
            log_4 = f'{logs[3][0].astimezone(timezone("Asia/baghdad")).strftime("%p %I:%M")}' if len(logs) >= 4 else ''
            query = f"""
                        SELECT he.name as emp_name,
                        hd.name as dep_name,
                        '{log_1}' as entry1,
                        '{log_2}' as out1,
                        '{log_3}' as entry2,
                        '{log_4}' as out2,
                        hwet.name as day_type,
                        oi.att_date,
                        oi.date_in,
                        oi.date_out,
                        (hlt.name ->> 'ar_001') as leave_name,
                        oa."diff_Exit",
                        oa.diff_entry
                        from hr_employee he
                        LEFT JOIN hr_work_entry hwe on he.id = hwe.employee_id 
                        AND '{(date1[0].isoformat())}' = Date(hwe.date_start)
                        LEFT JOIN hr_department hd ON hd.id = he.department_id
                        LEFT JOIN hr_work_entry_type hwet ON hwet.id = hwe.work_entry_type_id
                        LEFT JOIN od_inout oi ON oi.emp_deviceno = he.studio_employee_number
                        and oi.att_date = '{(date1[0].isoformat())}'
                        LEFT JOIN od_attpayroll oa ON oa.inout = oi.id
                        LEFT JOIN hr_leave hl ON hl.employee_id = he.id
                        and (hl.request_unit_half = TRUE OR hl.request_unit_hours = TRUE)
                        and hl.request_date_from = '{(date1[0].isoformat())}'
                        LEFT JOIN hr_leave_type hlt ON hlt.id = hl.holiday_status_id
                        AND hwet.code <> ANY (ARRAY['MISSION','LATE','LATE2','ERLYIN','ERLYOUT','ERLYIN2',
                        'OVT1','OVT2','OVT3','OVT4'])
                        where hwe.employee_id = '{employee_id.id}'
                        and hwe.state != 'cancelled'
            """
            # query = f"""SELECT he.name as emp_name,
            #                             hd.name as dep_name,
            #                             '{log_1}' as entry1,
            #                             '{log_2}' as out1,
            #                             '{log_3}' as entry2,
            #                             '{log_4}' as out2,
            #                             hwet.name as day_type,
            #                             oi.att_date,
            #                             oi.date_in,
            #                             oi.date_out,
            #                             (hlt.name ->> 'ar_001') as leave_name,
            #                             oa."diff_Exit",
            #                             oa.diff_entry
            #                             from hr_work_entry hwe
            #                             LEFT JOIN hr_employee he on he.id = hwe.employee_id
            #                             AND '{(date1[0].isoformat())}' = Date(hwe.date_start)
            #                             LEFT JOIN hr_department hd ON hd.id = he.department_id
            #                             LEFT JOIN hr_work_entry_type hwet ON hwet.id = hwe.work_entry_type_id
            #                             LEFT JOIN od_inout oi ON oi.emp_deviceno = he.studio_employee_number
            #                             and oi.att_date = '{(date1[0].isoformat())}'
            #                             LEFT JOIN od_attpayroll oa ON oa.inout = oi.id
            #                             LEFT JOIN hr_leave hl ON hl.employee_id = he.id
            #                             and (hl.request_unit_half = TRUE OR hl.request_unit_hours = TRUE)
            #                             and hl.request_date_from = '{(date1[0].isoformat())}'
            #                             LEFT JOIN hr_leave_type hlt ON hlt.id = hl.holiday_status_id
            #                             AND hwet.code <> ANY (ARRAY['MISSION','LATE','LATE2','ERLYIN','ERLYOUT','ERLYIN2',
            #                             'OUT1','OUT2','OUT3','OUT4'])
        	# 							and hwe.employee_id = '{employee_id.id}'
            # """
            self._cr.execute(query)
            rec = self._cr.dictfetchone()
            if rec and rec['date_in'] and rec['date_out']:
                print('in ', rec['date_in'], 'out ', rec['date_out'], rec['date_out'] - rec['date_in'])
            day = ''
            if date1[0].strftime('%A') == 'Sunday':
                day = 'الأحد '
            elif date1[0].strftime('%A') == 'Monday':
                day = 'الإثنين '
            elif date1[0].strftime('%A') == 'Tuesday':
                day = 'الثلاثاء '
            elif date1[0].strftime('%A') == 'Wednesday':
                day = 'الأربعاء '
            elif date1[0].strftime('%A') == 'Thursday':
                day = 'الخميس '
            elif date1[0].strftime('%A') == 'Friday':
                day = 'الجمعة '
            elif date1[0].strftime('%A') == 'Saturday':
                day = 'السبت '
            if rec:
                rec['date'] = day + date1[0].strftime('%m-%d')
                if rec['date_in'] and rec['date_out']:
                    rec['work_hours'] = (rec['date_out'] - rec['date_in'])
                fetched_data.append(rec)
        print('all fetched : ', fetched_data)
        return fetched_data

    def save_options(self):
        # print('report date', self.date.strftime('%Y-%m-%d'))
        fetched = self.fill_view_data(self.employee_name, self.start_date, self.end_date)
        total_hours = 0
        for rec in fetched:
            if rec.get('work_hours'):
                total_hours += rec['work_hours'].seconds / 3600
        total_hours = "{:.2f}".format(total_hours)
        print('total hours ', total_hours)
        data = {
            'allFetched': fetched,
            'employee_name': self.employee_name.name,
            'department_name': self.employee_name.department_id.name,
            'badge_number': self.employee_name.barcode,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_hours': total_hours
        }
        print('data ', data)
        return self.env.ref('ALTANMYA_Attendance_Reports.employee_monthly_attendance_action').report_action(self, data)
