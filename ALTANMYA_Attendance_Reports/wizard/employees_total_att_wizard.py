from odoo import models, fields, api
import calendar


class EmployeesTotalAttendanceReportWizard(models.TransientModel):
    _name = 'emp.total.att.wizard'

    def get_years(self):
        year_list = []
        for i in range(2020, 2040):
            year_list.append((i, str(i)))
        return year_list

    month = fields.Selection([('01', 'كانون الثاني'), ('02', 'شباط'), ('03', 'آذار'), ('04', 'نيسان'),
                              ('05', 'أيار'), ('06', 'حزيران'), ('07', 'تموز'), ('08', 'آب'),
                              ('9', 'أيلول'), ('10', 'تشرين الأول'), ('11', 'تشرين الثاني'), ('12', 'كانون الأول')],
                             string='الشهر')
    year = fields.Selection(selection='get_years', string='السنة')
    shift_ids = fields.Many2many('resource.calendar', string='الوردية')
    att_mode = fields.Selection([('standard', 'Standard mode'), ('daily', 'Daily mode'), ('classic', 'Classic mode'),
                                 ('sequential', 'Sequential mode'), ('shift', 'Shift mode')], string='نوع الحضور')

    def fill_report_data(self, att_mode, shifts):
        start_date = f"""{self.year}-{self.month}-01"""
        if self.month == '01' or self.month == '03' or self.month == '05' or self.month == '07' or self.month == '10' or self.month == '12':
            end_date = f"""{self.year}-{self.month}-31"""
        elif self.month == '02':
            end_date = f"""{self.year}-{self.month}-28"""
        else:
            end_date = f"""{self.year}-{self.month}-30"""
        print('dates ', start_date, end_date)
        where_clause = ''
        if not att_mode and not shifts:
            where_clause = ''
        elif not att_mode:
            where_clause = f"WHERE A.RESOURCE_CALENDAR_ID = ANY (ARRAY{shifts.ids})"
        elif not shifts:
            where_clause = f"WHERE A.ATT_MODE = '{att_mode}'"
        else:
            where_clause = f"WHERE A.RESOURCE_CALENDAR_ID = ANY (ARRAY{shifts.ids}) AND A.ATT_MODE = '{att_mode}'"
        # query to fetch the employee and his absent days
        query = f"""
                SELECT DISTINCT(A.id), A.name,
                COUNT(E.name) filter (where E.code = 'absent') as total_absent_days,
                (ROW_NUMBER() OVER (ORDER BY A.ID))
                FROM hr_employee A
                LEFT JOIN HR_WORK_ENTRY D ON D.EMPLOYEE_ID = A.ID 
                AND TO_CHAR(D.date_start, 'yyyy-mm-dd') >= '{start_date}'
                AND TO_CHAR(D.date_start, 'yyyy-mm-dd') <= '{end_date}'
                LEFT JOIN HR_WORK_ENTRY_TYPE E ON E.id = D.work_entry_type_id
                {where_clause}
                GROUP BY A.name, A.ID
                ORDER BY A.ID
                """
        self.env.cr.execute(query)
        fetched_data = self._cr.dictfetchall()
        if not att_mode and not shifts:
            shifts_domain = (True, '=', True)
            att_mode_domain = (True, '=', True)
        elif not att_mode and shifts:
            att_mode_domain = (True, '=', True)
            shifts_domain = ('resource_calendar_id', 'in', shifts.ids)
        elif not shifts and att_mode:
            shifts_domain = (True, '=', True)
            att_mode_domain = ('att_mode', '=', att_mode)
        else:
            shifts_domain = ('resource_calendar_id', 'in', shifts.ids)
            att_mode_domain = ('att_mode', '=', att_mode)
        employees = self.env['hr.employee'].search(
            [('active', 'in', [True, False]), shifts_domain, att_mode_domain])
        print('emp count', self.env['hr.employee'].search_count([]))

        # query to fetch the employee's total late hours and convert them to business days
        for emp in employees:
            qry = self.env.cr.execute(f"""
                    SELECT DISTINCT(Att_date), OA.diff_entry
                    FROM OD_ATTPAYROLL OA
                    WHERE OA.EMPLOYEE_ID = {emp.id}
                    AND OA.ATT_DATE >= '{start_date}' AND OA.ATT_DATE <= '{end_date}'
                    """)
            total_late = self._cr.dictfetchall()
            total_employee_late_entry = 0
            total_hours = 0
            total_minutes = 0
            for late in total_late:
                if late['diff_entry'] and late['diff_entry'][0] == '-':
                    print('diff ', late['diff_entry'])
                    print('ll ', late['diff_entry'][1:3], int(late['diff_entry'][1:3]) * 60)
                    print('uu ', late['diff_entry'][4:6])
                    total_employee_late_entry += (int(late['diff_entry'][1:3]) * 60) + int(late['diff_entry'][4:6])
                    total_hours = int(total_employee_late_entry / 60)
                    total_minutes = int((total_employee_late_entry % 60))
            print('emp name ', emp.name, int(total_employee_late_entry / 60), (total_employee_late_entry % 60))
            for rec in fetched_data:
                if rec['name'] == emp.name:
                    print('hoo', rec['name'], emp.name, total_hours)
                    total = str(total_hours) + ':' + str(total_minutes)
                    if total_hours == 0 and total_minutes == 0:
                        total = '-'
                        rec['total_late_days'] = '-'
                    rec['total_late_hours'] = total
                    print('total hooours ', total_hours)
                    if not rec.get('total_late_days'):
                        rec['total_late_days'] = str(int(total_hours / 8))
                    print("rec['total_late_days'] ", rec['total_late_days'])
            print('tot ', total_employee_late_entry / 60)
        return fetched_data

    def save_options(self):
        data = {
            'month': self.month,
            'year': self.year,
            'fetched_data': self.fill_report_data(self.att_mode, self.shift_ids)
        }
        print('data ', data)
        return self.env.ref('ALTANMYA_Attendance_Reports.employees_total_attendance_action').report_action(self, data)
