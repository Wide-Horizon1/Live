from odoo import models, fields, api
import pytz
from pytz import timezone, utc
import base64
import xlrd
from odoo.exceptions import UserError
import datetime
from xlrd.xldate import xldate_as_datetime
from datetime import timedelta


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    check_work_entry = fields.Boolean(default=False, string='Working Entry')
    overTime = fields.Many2one('hr.work.entry.type')
    Late = fields.Many2one('hr.work.entry.type')
    atten = fields.Many2one('hr.work.entry.type')
    Get_out_early = fields.Many2one('hr.work.entry.type')
    Show_out_early = fields.Boolean(default=False, string='Show Out Early')
    actual_working_hours = fields.Char(string='actual working hours:', default='08:00')
    day_start = fields.Char(string='Day Start at:', default='08:00')
    Max = fields.Boolean(default=True, string='Working hours are 8 hours maximum')
    start_d = fields.Char(string='Work starts at:', default='08:00')
    end_d = fields.Char(string='Work ends at:', default='17:00')
    Break = fields.Boolean(default=True, string='Break hours At :')
    start_break = fields.Char(string='Work break at:', default='12:00')
    end_break = fields.Char(string='Work break at:', default='13:00')


class ExcelData(models.Model):
    _name = 'excel.data'
    _description = 'Excel Data'

    approval_request_id = fields.Many2one('approval.request')
    employee = fields.Char(string='Employee', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    start_hour = fields.Char(string='Start Hour', readonly=True)
    end_hours = fields.Char(string='End Hours', readonly=True)
    late = fields.Char(string='Late')
    overtime = fields.Float(string='Overtime')
    apporvlelateee = fields.Boolean(default=True, string='Approval Late')
    apporvleovertime = fields.Boolean(default=True, string='Approval OverTime')


class EmployeesAttendanceReportWizard(models.TransientModel):
    _name = 'work.entry.inh.wizard'

    excel_file = fields.Binary(string='Excel File', required=True)
    approver_ids = fields.Many2many('res.users', string="Approvers", required=True)

    def import_excel_data(self):

        excel_data = self.excel_file
        print('excel_data..', excel_data)
        # user_ids = self.approver_ids.mapped('id')
        # print('user_ids==>', user_ids)

        # *********************************************#
        workbook = xlrd.open_workbook(file_contents=base64.b64decode(excel_data))
        print('workbook..', workbook)

        # Get the first sheet by index (assuming it's the first sheet)
        sheet = workbook.sheet_by_index(0)
        print('sheet..', sheet)
        # Get column names from the first row
        column_names = [cell.value for cell in sheet.row(0)]
        print('column_names..', column_names)
        # Check if all required columns are present
        required_columns = ['employee', 'date', 'start_hour', 'end_hours', 'late', 'overtime']

        # approval_category = self.env['approval.category'].search([('name', '=', 'work entry')], limit=1)
        # # Create the approval request
        # approval_request = self.env['approval.request'].sudo().create({
        #     'name': 'New Approval Request',
        #     'category_id': approval_category.id,
        #     'attachment': excel_data,
        #     'request_owner_id': self.env.user.id
        # })
        # print('approval_request..', approval_request)

        if not all(column in column_names for column in required_columns):
            raise UserError("The Excel file does not contain all the required columns.")
        # Iterate through the rows starting from the second row
        for row_index in range(1, sheet.nrows):
            row = sheet.row_values(row_index)
            # Extract the data from each column based on the column names
            employee = row[0]
            date = row[1]
            dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(row[1], workbook.datemode))
            start_hour = row[2]
            print('Type of start_hour:', type(row[2]))
            print('Value of start_hour:', row[2])
            if isinstance(start_hour, float):
                hour = int(start_hour * 24)
                print('hour==>', hour)
                minute = int((start_hour * 24 * 60) % 60)
                print('minute==>', minute)
                start_hour = datetime.time(hour=hour, minute=minute)
            else:
                start_hour = datetime.datetime.strptime(start_hour, '%I:%M:%S %p').time()

            end_hours = row[3]

            if isinstance(end_hours, float):
                hour = int(end_hours * 24)
                print('hour==>', hour)
                minute = int((end_hours * 24 * 60) % 60)
                print('minute==>', minute)
                end_hours = datetime.time(hour=hour, minute=minute)
            else:
                end_hours = datetime.datetime.strptime(end_hours, '%I:%M:%S %p').time()
            late = row[4]
            if isinstance(late, float):
                hour = int(late * 24)
                print('hour==>', hour)
                minute = int((late * 24 * 60) % 60)
                print('minute==>', minute)
                late = datetime.time(hour=hour, minute=minute)
            else:
                late = datetime.datetime.strptime(late, '%I:%M:%S %p').time()
            overtime = row[5]
            print('start_hour--->', start_hour.strftime('%H:%M'))
            print('late--->', late.strftime('%H:%M'))
            print('end_hours--->', end_hours.strftime('%H:%M'))
            gcc = self.env['excel.data'].sudo().create({
                # 'approval_request_id': approval_request.id,
                'employee': employee,
                'date': dt,
                'start_hour': start_hour,
                'end_hours': end_hours,
                'late': late,
                'overtime': overtime,
                'apporvlelateee': 'True',
                'apporvleovertime': 'True',
            })

            # TODO: Create a work entry using the extracted data

        # Print the data
        print('Row Data:', employee, date, start_hour, end_hours, late, overtime)
        # *********************************************#

        # Create work entries using the extracted data


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'
    excel_data_ids = fields.One2many('excel.data', 'approval_request_id', string='Excel Data')
    approval_request_show_id = fields.One2many('show.data', 'approval_request_id', string='show Data')
    approval_request_show_details = fields.One2many('show.details', 'approval_request_id', string='show Details')
    all_data_ids = fields.One2many('send.data', 'approval_request_id', string='Excel Data')
    date_from = fields.Date('date_from')
    date_to = fields.Date('date_to')

    def action_approve(self, approver=None):
        if self.category_id.atten and self.category_id.Late and self.category_id.overTime and self.category_id.Get_out_early:
            super(ApprovalRequest, self).action_approve(approver=approver)

            for excel_data in self.excel_data_ids:
                employee = excel_data.employee
                date = excel_data.date
                dt = date  # Assuming dt field in excel.data is already a datetime value
                start_hour = excel_data.start_hour
                end_hours = excel_data.end_hours
                late = excel_data.late
                overtime = excel_data.overtime
                oprolate = excel_data.apporvlelateee
                oproovertime = excel_data.apporvleovertime

                print('start_hour ', start_hour)
                print('type start_hour ', type(start_hour))
                print('date ', date)
                print('type  ', type(date))

                #### m3aljt al data ###
                print('end_hours==>', start_hour)
                d_start = start_hour  # Assuming this is the string value of end_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the end_hours string to a time object
                d_start_time = datetime.datetime.strptime(d_start, '%H:%M:%S').time()

                # Combine the date and time into a datetime object
                start_data_datetime = datetime.datetime.combine(date_datetime, d_start_time)
                print('start_data_datetime==>', start_data_datetime)
                start_dd = start_data_datetime - datetime.timedelta(hours=3)
                formatted_start_date_hours = start_dd.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_start_date_hours:', formatted_start_date_hours)

                #### m3aljt al data ###

                ########## start get end_houer from excel #########
                print('end_hours==>', end_hours)
                end_hours_str = end_hours  # Assuming this is the string value of end_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the end_hours string to a time object
                end_hours_time = datetime.datetime.strptime(end_hours_str, '%H:%M:%S').time()

                # Combine the date and time into a datetime object
                end_datetime = datetime.datetime.combine(date_datetime, end_hours_time)
                print('end_datetime==>', end_datetime)
                end = end_datetime - datetime.timedelta(hours=3)
                formatted_end_hours = end.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_end_hours:', formatted_end_hours)
                ########### end get end_houer from excel ###########

                leaves_work_entry_gg = self.env['hr.work.entry'].search(
                    [('date_start', '>=', formatted_start_date_hours), ('date_stop', '<=', formatted_end_hours),
                     ('leave_id', '!=', False), ('employee_id', '=',
                                                 self.env['hr.employee'].search(
                                                     ['|', ('name', '=', employee),
                                                      ('registration_number', '=', employee.split('.')[0])],
                                                     limit=1).id)])

                print('leaves_work_entry_gg==>', leaves_work_entry_gg)
                if leaves_work_entry_gg:
                    continue
                if not oprolate:
                    late = 0

                if not oproovertime:
                    overtime = 0
                print('lateeeee,', late)

                print('Row Data:', dt, employee, date, start_hour, end_hours, late, overtime)
                # Convert date_value to a datetime object
                # get date and combine him (start at 8 am)
                date_start = datetime.datetime.combine(date, datetime.time(hour=5, minute=0, second=0))
                # get date and replace after combine  (start at 12 am)
                date_stop_break = date_start.replace(hour=9, minute=0, second=0)
                # get date and replace after combine  (start at 1 pm)
                date_start_after_break = date_start.replace(hour=10, minute=0, second=0)
                # get date and replace after combine  (start at 5 pm)
                date_stop = date_start.replace(hour=13, minute=0, second=0)

                # Set the timezone to UTC
                timezone = pytz.timezone('UTC')

                # Convert datetime values to timezone-aware datetime
                date_start_timezone = timezone.localize(date_start)
                date_start_timezone_after_break = timezone.localize(date_start_after_break)
                date_stop_timezone_break = timezone.localize(date_stop_break)
                date_stop_timezone = timezone.localize(date_stop)

                # Convert timezone-aware datetime to UTC naive datetime
                date_start_naive = date_start_timezone.astimezone(pytz.UTC).replace(tzinfo=None)
                date_stop_naive_breack = date_stop_timezone_break.astimezone(pytz.UTC).replace(tzinfo=None)
                date_start_naive_after_breack = date_start_timezone_after_break.astimezone(pytz.UTC).replace(
                    tzinfo=None)
                date_stop_naive = date_stop_timezone.astimezone(pytz.UTC).replace(tzinfo=None)
                print('date_start_naive', date_start_naive)
                print('type [ date_start_naive', type(date_start_naive))
                print('date_stop_naive_breack', date_stop_naive_breack)
                print('date_stop_naive', date_stop_naive)
                print('date_start_naive_after_breack', date_start_naive_after_breack)
                print('type date_start_naive_after_breack', type(date_start_naive_after_breack))
                existing_work_entries = self.env['hr.work.entry'].search([
                    ('employee_id', '=',
                     self.env['hr.employee'].search(
                         ['|', ('name', '=', employee), ('registration_number', '=', employee.split('.')[0])],
                         limit=1).id),
                    ('date_start', '>=', date_start_naive.replace(hour=0, minute=0, second=0)),
                    ('date_stop', '<=', date_start_naive.replace(hour=23, minute=59, second=59)),
                    ('leave_id', '=', False)
                ])
                print('existing_work_entries...', existing_work_entries)
                # Delete existing work entries
                existing_work_entries.unlink()
                print('after delete existing_work_entries...', existing_work_entries)

                ########## start get start_hour from input: ###########
                start_date = self.category_id.start_d
                start_hours_inp = start_date  # Assuming this is the string value of start_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the start_hours string to a time object
                start_hours_time_inp = datetime.datetime.strptime(start_hours_inp, '%H:%M').time()

                # Combine the date and time into a datetime object
                start_datetime_inp = datetime.datetime.combine(date_datetime, start_hours_time_inp)
                start_inp = start_datetime_inp - datetime.timedelta(hours=3)
                formatted_start_hours_input = start_inp.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_start_hours_input:', formatted_start_hours_input)
                print('type formatted_start_hours_input:', type(formatted_start_hours_input))
                formatted_start_hurrr_input_obj = datetime.datetime.strptime(formatted_start_hours_input,
                                                                             '%Y-%m-%d %H:%M:%S')

                print('type formatted_start_hurrr_input_obj:', type(formatted_start_hurrr_input_obj))

                ########### end hour in day from input ######

                # ########## start get actual start_hour from input: ###########
                work_h_in_day = self.category_id.actual_working_hours
                start_calc_h_in_daya = work_h_in_day  # Assuming this is the string value of start_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the start_hours string to a time object
                start_hours_in_day = datetime.datetime.strptime(start_calc_h_in_daya, '%H:%M').time()

                # Combine the date and time into a datetime object
                start_datetime_h_ing_day = datetime.datetime.combine(date_datetime, start_hours_in_day)
                start_inp_h_in_day = start_datetime_h_ing_day - datetime.timedelta(hours=3)
                formatted_start_hours_in_day = start_inp_h_in_day.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_start_hours_in_day:', formatted_start_hours_in_day)
                print('type formatted_start_hours_in_day:', type(formatted_start_hours_in_day))
                formatted_start_in_one_day = datetime.datetime.strptime(formatted_start_hours_in_day,
                                                                        '%Y-%m-%d %H:%M:%S')
                formatted_start_in_one_day += datetime.timedelta(hours=3)

                print('type formatted_start_in_one_day:', type(formatted_start_in_one_day))
                print('formatted_start_in_one_day', formatted_start_in_one_day)

                ########### end get  actual hour in day  from input ######

                ########## start get start_break from input: ###########
                start_break = self.category_id.start_break
                start_break_inp = start_break  # Assuming this is the string value of start_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the start_hours string to a time object
                start_break_time_inp = datetime.datetime.strptime(start_break_inp, '%H:%M').time()

                # Combine the date and time into a datetime object
                start_datetime_break_inp = datetime.datetime.combine(date_datetime, start_break_time_inp)
                start_inp_b = start_datetime_break_inp - datetime.timedelta(hours=3)
                formatted_start_break_input = start_inp_b.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_start_break_input:', formatted_start_break_input)
                print('type formatted_start_break_input:', type(formatted_start_break_input))
                formatted_start_break_input_obj = datetime.datetime.strptime(formatted_start_break_input,
                                                                             '%Y-%m-%d %H:%M:%S')
                print('type formatted_start_break_input_obj:', type(formatted_start_break_input_obj))

                ########### end get start_break from input ######

                ########## start get start_break from input: ###########
                end_break = self.category_id.end_break
                end_break_inp = end_break  # Assuming this is the string value of start_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the start_hours string to a time object
                end_break_time_inp = datetime.datetime.strptime(end_break_inp, '%H:%M').time()

                # Combine the date and time into a datetime object
                end_datetime_break_inp = datetime.datetime.combine(date_datetime, end_break_time_inp)
                end_inp_b = end_datetime_break_inp - datetime.timedelta(hours=3)
                formatted_end_break_input = end_inp_b.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_end_break_input:', formatted_end_break_input)
                formatted_end_break_input_obj = datetime.datetime.strptime(formatted_end_break_input,
                                                                           '%Y-%m-%d %H:%M:%S')

                print('type formatted_end_break_input_obj:', type(formatted_end_break_input_obj))
                ########### end get start_break from input ######

                ########## start get start_day from input: ###########
                start_day = self.category_id.day_start
                start_day_inp = start_day  # Assuming this is the string value of start_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the start_hours string to a time object
                start_day_time_inp = datetime.datetime.strptime(start_day_inp, '%H:%M').time()

                # Combine the date and time into a datetime object
                start_datetime_day_inp = datetime.datetime.combine(date_datetime, start_day_time_inp)
                start_inp_d = start_datetime_day_inp - datetime.timedelta(hours=3)
                formatted_start_day_input = start_inp_d.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_start_day_input:', formatted_start_day_input)
                formatted_start_day_input_obj = datetime.datetime.strptime(formatted_start_day_input,
                                                                           '%Y-%m-%d %H:%M:%S')

                print('type formatted_start_day_input_obj:', type(formatted_start_day_input_obj))
                ########### end get start_day  from input ######

                ######## start work entry Late#############
                getLate = self.category_id.Late
                checkmax = self.category_id.Max
                print('lateeeee,', late)
                print('type lateeeee,', type(late))
                # # Check if there is a delay value
                if late:
                    # late_hours = float(late.split(':')[0])
                    late_hours = late
                    if late_hours != '00:00:00':
                        # print('timedelta(hours=late_hours),,',timedelta(hours=late_hours))
                        print('late_hours,,', late_hours)
                        late_start = formatted_start_hurrr_input_obj if checkmax else formatted_start_day_input_obj
                        print('late_start', late_start)
                        print('type late_start', type(late_start))
                        hours, minutes, seconds = map(int, late_hours.split(':'))
                        late_duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                        late_stop = late_start + late_duration
                        late_work_entry_type_id = self.env['hr.work.entry.type'].search([('code', '=', 'DELAY')]).id
                        print('late_stop==>', late_stop)
                        print('late_duration==>', late_duration)
                        res = ""
                        for c in employee:
                            if c != ".":
                                res += c
                            else:
                                break
                        print(' res ', res)
                        employee_domain = ['|', ('name', '=', employee),
                                           ('registration_number', '=', res)]
                        employee_record = self.env['hr.employee'].search(employee_domain, limit=1)
                        print(' employee_domain..==>', employee_domain)
                        print('employee_record..==>', employee_record)
                        late_work_entry = self.env['hr.work.entry'].create({
                            'name': 'late',
                            'employee_id': employee_record.id,
                            'work_entry_type_id': getLate.id,
                            'date_start': late_start,
                            'date_stop': late_stop,
                        })

                        date_start_naive = late_stop  # Update the start time to be after the delay
                        formatted_start_hours_input = late_stop
                        formatted_start_day_input_obj = late_stop
                        formatted_start_hurrr_input_obj = late_stop
                        print('date_start_naive new', date_start_naive)
                        print('formatted_start_hours_input new', formatted_start_hours_input)
                        ############## end work entry type late ##########

                ########## start work entry Attendence ##########
                getAtten = self.category_id.atten
                checkmax = self.category_id.Max
                start_date = self.category_id.start_d
                end_date = self.category_id.end_d
                print('checkmax==>', checkmax)
                print('start_date==>', start_date)
                print('end_date==>', end_date)

                ########## start get end_houer from excel #########
                print('end_hours==>', end_hours)
                end_hours_str = end_hours  # Assuming this is the string value of end_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the end_hours string to a time object
                end_hours_time = datetime.datetime.strptime(end_hours_str, '%H:%M:%S').time()

                # Combine the date and time into a datetime object
                end_datetime = datetime.datetime.combine(date_datetime, end_hours_time)
                print('end_datetime==>', end_datetime)
                end = end_datetime - datetime.timedelta(hours=3)
                formatted_end_hours = end.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_end_hours:', formatted_end_hours)
                ########### end get end_houer from excel ###########

                ########## start get end_hour from input: ###########
                end_hours_inp = end_date  # Assuming this is the string value of end_hours
                date_datetime = date  # Assuming this is already a datetime.date object

                # Convert the end_hours string to a time object
                end_hours_time_inp = datetime.datetime.strptime(end_hours_inp, '%H:%M').time()

                # Combine the date and time into a datetime object
                end_datetime_inp = datetime.datetime.combine(date_datetime, end_hours_time_inp)
                end_inp = end_datetime_inp - datetime.timedelta(hours=3)
                formatted_end_hours_input = end_inp.strftime('%Y-%m-%d %H:%M:%S')
                print('formatted_end_hours_input:', formatted_end_hours_input)
                ########### end get end_hour from input ######

                res = ""
                for c in employee:
                    if c != ".":
                        res += c
                    else:
                        break
                print(' res ', res)
                print('date_stop_naive ', date_stop_naive)
                print('date_stop_naive_breack ', date_stop_naive_breack)
                print('date_start_naive_after_breack ', date_start_naive_after_breack)
                # get employee name or number
                employee_domain = ['|', ('name', '=', employee), ('registration_number', '=', res)]
                employee_record = self.env['hr.employee'].search(employee_domain, limit=1)
                print('2employee_domain..==>', employee_domain)
                print('2employee_record..==>', employee_record)
                work_entry = self.env['hr.work.entry'].create({
                    'name': 'attendance',
                    'employee_id': employee_record.id,
                    'work_entry_type_id': getAtten.id,
                    'date_start': formatted_start_hurrr_input_obj if checkmax else formatted_start_day_input_obj,
                    'date_stop': formatted_start_break_input,
                })
                # time bettwen start and start data break
                calc_1 = formatted_start_break_input_obj - date_start_naive
                formatted_end_hours_dt = datetime.datetime.strptime(formatted_end_hours, '%Y-%m-%d %H:%M:%S')

                # work hour (يعني ايمتا فات وايمتا طلع وهاد الشي يعني متضمن التاخير)
                calc_2 = formatted_end_hours_dt - date_start_naive

                # work hour -  break (هي مشان تيجب اديش ساعات العمل الفعلي)
                oodoo = '01:00:00'  # total breck time
                totoal_breack_time = formatted_end_break_input_obj - formatted_start_break_input_obj
                print('totoal_breack_time==>', totoal_breack_time)
                hours, minutes, seconds = map(int, oodoo.split(':'))
                late_durationnnn = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                calc_late = calc_2 - totoal_breack_time
                print('late==>', late)
                print('calc_late==>', calc_late)
                print('late_duration==>', totoal_breack_time)
                print('calc_2 ddd==>', calc_2)
                print('type calc_late==>', type(calc_late))
                print('type late_duration==>', type(totoal_breack_time))
                print('type calc_2==>', type(calc_2))

                # time work hour - sa3at al 3ml al 9ba7eh(work before break)
                calc_3 = calc_2 - calc_1

                # time 8 sa3at
                calc_4 = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
                calc_4_datetime = datetime.datetime.combine(date_datetime, calc_4)
                print('type calc_4', type(calc_4))
                print('calc_4', calc_4)
                print('type calc_4_datetime', type(calc_4_datetime))
                print('calc_4_datetime', calc_4_datetime)

                # 8h - sa3at al 3ml al 9ba7eh(work before break)
                calc_5 = formatted_start_in_one_day - calc_1
                # calc_6 = date_start_naive_after_breack + datetime.timedelta(hours=calc_5.hour, minutes=calc_5.minute,
                #                                                             seconds=calc_5.second)

                calc_6 = formatted_end_break_input_obj + datetime.timedelta(hours=calc_5.hour, minutes=calc_5.minute,
                                                                            seconds=calc_5.second)

                # 7sbt al calc_7
                calc_7_b = '00:00:00'
                hours, minutes, seconds = map(int, calc_7_b.split(':'))
                calc_7 = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                print('before calc_7==>', calc_7)

                c_remaning = '-10:-10:00'
                hours, minutes, seconds = map(int, c_remaning.split(':'))
                calc_remaning = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                print('datetime.timedelta(hours=formatted_start_in_one_day.hour):',
                      datetime.timedelta(hours=formatted_start_in_one_day.hour))
                if calc_late > datetime.timedelta(hours=formatted_start_in_one_day.hour):
                    print('tototo')
                    print('calc_late toto', calc_late)
                    calc_7 = calc_late - datetime.timedelta(hours=formatted_start_in_one_day.hour,
                                                            minutes=formatted_start_in_one_day.minute,
                                                            seconds=formatted_start_in_one_day.second)
                    print('calc_7 toto', calc_7)
                # 7sbt al remanig time (هي بتحسب اذا الواحد طلع بكير ولسا ما كمل ال 8 ساعات)

                else:
                    calc_remaning = datetime.timedelta(hours=formatted_start_in_one_day.hour,
                                                       minutes=formatted_start_in_one_day.minute,
                                                       seconds=formatted_start_in_one_day.second) - calc_late
                    print('calc_remaning', calc_remaning)

                print('calc==>', calc_1)
                print('eee calc_2==>', calc_2)
                print('calc_3==>', calc_3)
                print('type calc_3==>', type(calc_3))
                print('calc_4==>', calc_4)
                print('calc_4_datetime==>', calc_4_datetime)
                print('calc_5==>', calc_5)
                print('calc_6', calc_6)
                print('calc_7', calc_7)
                print('type calc_6', type(calc_6))

                if calc_late < datetime.timedelta(hours=formatted_start_in_one_day.hour,
                                                  minutes=formatted_start_in_one_day.minute,
                                                  seconds=formatted_start_in_one_day.second):
                    time_to_end = formatted_end_hours_dt
                    print('how much==>', time_to_end)
                    print('formatted_end_hours_dt test==>', formatted_end_hours_dt)
                else:
                    time_to_end = calc_6
                    print('else time_to_end==>', time_to_end)

                mmpp = formatted_end_hours_input
                ####check if have lower than 8 houer when check true ###
                if formatted_end_hours < formatted_end_hours_input:
                    print('nice we did it==>')
                    mmpp = formatted_end_hours
                ######start create ########

                work_entry = self.env['hr.work.entry'].create({
                    'name': 'attendance',
                    'employee_id': employee_record.id,
                    'work_entry_type_id': getAtten.id,
                    'date_start': date_start_naive_after_breack,
                    'date_stop': mmpp if checkmax else time_to_end,
                })
                getoutetly = self.category_id.Get_out_early
                Show_out_early = self.category_id.Show_out_early
                if Show_out_early:
                    if calc_remaning > datetime.timedelta(hours=0, minutes=0):
                        after_rem = calc_remaning + time_to_end
                        print('after_rem==>', after_rem)
                        work_entry = self.env['hr.work.entry'].create({
                            'name': 'get out early',
                            'employee_id': employee_record.id,
                            'work_entry_type_id': getoutetly.id,
                            'date_start': mmpp if checkmax else time_to_end,
                            'date_stop': after_rem,
                        })

                ######## end  work entry Attendence #############
                # 'date_stop': date_stop_naive if checkmax else formatted_end_hours,

                # Check if overtime has a value

                ########### start work entry overTime ########
                cc = self.category_id.overTime
                res = ""
                for c in employee:
                    if c != ".":
                        res += c
                    else:
                        break

                if not checkmax:
                    print('ksksks')
                    if calc_7 > datetime.timedelta(hours=0, minutes=0):
                        print('momomomo')
                        overtime_start = time_to_end
                        print('time_to_end over', time_to_end)
                        overtime_stop = overtime_start + calc_7
                        print('overtime_stop over', overtime_stop)
                        employee_domain = ['|', ('name', '=', employee), ('registration_number', '=', res)]
                        employee_record = self.env['hr.employee'].search(employee_domain, limit=1)
                        print('3employee_domain..==>', employee_domain)
                        print('3employee_record..==>', employee_record)
                        overtime_work_entry = self.env['hr.work.entry'].create({
                            'name': 'Overtime',
                            'employee_id': employee_record.id,
                            'work_entry_type_id': cc.id,
                            'date_start': overtime_start,
                            'date_stop': overtime_stop,
                        })

                elif overtime and checkmax:
                    overtime_hours = float(overtime)
                    if overtime_hours > 0:
                        print("formatted_end_hours_input: ", formatted_end_hours_input)
                        # Extract the time portion from the formatted_end_hours_input
                        time_str = formatted_end_hours_input.split(' ')[-1]
                        hours, minutes, seconds = map(int, time_str.split(':'))
                        overtime_start = datetime.datetime(date_stop_naive.year, date_stop_naive.month,
                                                           date_stop_naive.day, hours, minutes, seconds)
                        overtime_duration = datetime.timedelta(
                            hours=overtime_hours)  # Assuming overtime duration is in hours
                        overtime_stop = overtime_start + overtime_duration
                        print('overtime_stop:', overtime_stop)
                        employee_domain = ['|', ('name', '=', employee),
                                           ('registration_number', '=', res)]
                        employee_record = self.env['hr.employee'].search(employee_domain, limit=1)
                        print('3employee_domain..==>', employee_domain)
                        print('3employee_record..==>', employee_record)
                        print('overtime_stop..==>', overtime_stop)
                        overtime_work_entry = self.env['hr.work.entry'].create({
                            'name': 'Overtime',
                            'employee_id': employee_record.id,
                            'work_entry_type_id': cc.id,
                            'date_start': formatted_end_hours_input,
                            'date_stop': overtime_stop,
                        })
        else:
            raise UserError("please chose work entry type from approval type")
