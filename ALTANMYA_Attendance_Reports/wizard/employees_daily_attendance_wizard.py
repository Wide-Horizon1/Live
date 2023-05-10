from odoo import models, fields, api


class EmployeesAttendanceReportWizard(models.TransientModel):
    _name = 'emp.daily.att.wizard'

    date = fields.Date(string='تاريخ الحضور')
    shift_ids = fields.Many2many('resource.calendar', string='الوردية')
    att_mode = fields.Selection([('standard', 'Standard mode'), ('daily', 'Daily mode'), ('classic', 'Classic mode'),
                                 ('sequential', 'Sequential mode'), ('shift', 'Shift mode')], string='نوع الحضور')

    def fill_attendance_records(self, att_date, shift, att_mode):
        where_clause = ''
        if not att_mode and not shift:
            where_clause = ''
        elif not att_mode:
            where_clause = f"WHERE C.SHIFT = ANY (ARRAY{shift.ids})"
        elif not shift:
            where_clause = f"WHERE C.ATT_MODE = '{att_mode}'"
        else:
            where_clause = f"WHERE C.SHIFT = ANY (ARRAY{shift.ids}) AND C.ATT_MODE = '{att_mode}'"
        query = f"""
                    SELECT C.EMPLOYEE_ID,
            		C.STUDIO_EMPLOYEE_NUMBER,
            		D.EMP_DEVICENO,
            		D.ATT_DATE,
            		C.BADGE_NUMBER,
            		C.EMPLOYEE_NAME,
            		C.DEPARTMENT_NAME,
            		D.IN_HOUR,
            		D.OUT_HOUR,
            		E.leave_duration,
            		E.leave_name,
            		D.diff_entry
            FROM
            	(SELECT A.ID AS EMPLOYEE_ID,
            			A.STUDIO_EMPLOYEE_NUMBER,
            			A.BARCODE AS BADGE_NUMBER,
            			A.NAME AS EMPLOYEE_NAME,
            			A.RESOURCE_CALENDAR_ID AS SHIFT,
            			A.ATT_MODE AS ATT_MODE,
            			B.NAME AS DEPARTMENT_NAME
            		FROM HR_EMPLOYEE AS A
            		LEFT JOIN HR_DEPARTMENT AS B ON A.DEPARTMENT_ID = B.ID) AS C
            LEFT JOIN
            	(SELECT OI.ATT_DATE,
			        OI.EMP_DEVICENO,
	 		        oa.diff_entry,
			        MIN(to_char((OI.DATE_IN AT TIME ZONE 'UTC+1'),'HH:MI')) AS IN_HOUR,
            		MAX(to_char((OI.DATE_OUT AT TIME ZONE 'UTC+1'),'HH:MI')) AS OUT_HOUR
		            FROM OD_INOUT OI, od_attpayroll oa
	 	            WHERE OI.id = oa.inout and OI.ATT_DATE = '{att_date}'
		            GROUP BY OI.ATT_DATE, OI.EMP_DEVICENO, oa.diff_entry
		            ORDER BY OI.EMP_DEVICENO) AS D ON C.STUDIO_EMPLOYEE_NUMBER = D.EMP_DEVICENO
            LEFT JOIN
                (SELECT (HLT.name ->> 'ar_001') AS leave_name,
		        HL.employee_id,
		        hl.request_date_from,
		        hl.duration_display as leave_duration
		        FROM HR_LEAVE HL, HR_LEAVE_TYPE HLT WHERE HL.holiday_status_id = HLT.id
                AND (HL.request_unit_hours = 'true' OR HL.request_unit_half = 'true'))
                AS E ON C.EMPLOYEE_ID = E.employee_id AND E.request_date_from = '{att_date}'
           {where_clause}
        """
        self._cr.execute(query)
        fetched_data = self._cr.dictfetchall()
        print('fetched date ', fetched_data)
        return fetched_data

    def save_options(self):
        # self.fill_attendance_records(self.date, self.shift_id, self.att_mode)
        # employees_records = self.env["employees.daily.attendance.report"].search_read([])
        print('report date', self.date.strftime('%Y-%m-%d'))
        data = {
            'report_date': self.date,
            # 'records': employees_records,
            'fetchedData': self.fill_attendance_records(self.date, self.shift_ids, self.att_mode)
        }
        print('data ', data)
        return self.env.ref('ALTANMYA_Attendance_Reports.employees_daily_attendance_action').report_action(self, data)
