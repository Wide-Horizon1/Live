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
    overTime = fields.Many2one('hr.work.entry.type')
    Late = fields.Many2one('hr.work.entry.type')
    atten = fields.Many2one('hr.work.entry.type')
    Max = fields.Boolean(default=True, string='Working hours are 8 hours maximum')
    start_d = fields.Char(string='Work starts at:', default='08:00')
    end_d = fields.Char(string='Work ends at:', default='17:00')


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
    all_data_ids = fields.One2many('send.data', 'approval_request_id', string='Excel Data')
    date_from = fields.Date('date_from')
    date_to = fields.Date('date_to')

    def action_approve(self, approver=None):
        if self.category_id.atten and self.category_id.Late and self.category_id.overTime:
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
                date_stop = date_start.replace(hour=14, minute=0, second=0)

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
                print('date_stop_naive_breack', date_stop_naive_breack)
                print('date_stop_naive', date_stop_naive)
                print('date_start_naive_after_breack', date_start_naive_after_breack)
                existing_work_entries = self.env['hr.work.entry'].search([
                    ('employee_id', '=',
                     self.env['hr.employee'].search(
                         ['|', ('name', '=', employee), ('registration_number', '=', employee.split('.')[0])],
                         limit=1).id),
                    ('date_start', '>=', date_start_naive.replace(hour=0, minute=0, second=0)),
                    ('date_stop', '<=', date_start_naive.replace(hour=23, minute=59, second=59)),
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
                ########### end get start_hour from input ######

                ######## start work entry Late#############
                getLate = self.category_id.Late

                print('lateeeee,', late)
                # # Check if there is a delay value
                if late:
                    # late_hours = float(late.split(':')[0])
                    late_hours = late
                    if late_hours != '00:00:00':
                        # print('timedelta(hours=late_hours),,',timedelta(hours=late_hours))
                        print('late_hours,,', late_hours)
                        late_start = date_start_naive
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
                    'date_start': formatted_start_hours_input if checkmax else date_start_naive,
                    'date_stop': date_stop_naive_breack,
                })
                calc_1 = date_stop_naive_breack - date_start_naive
                formatted_end_hours_dt = datetime.datetime.strptime(formatted_end_hours, '%Y-%m-%d %H:%M:%S')
                calc_2 = formatted_end_hours_dt - date_start_naive
                calc_3 = calc_2 - calc_1
                calc_4 = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
                calc_4_datetime = datetime.datetime.combine(date_datetime, calc_4)
                calc_5 = calc_4_datetime - calc_1
                calc_6 = date_start_naive_after_breack + datetime.timedelta(hours=calc_5.hour, minutes=calc_5.minute,
                                                                            seconds=calc_5.second)


                calc_7 = calc_2 - datetime.timedelta(hours=calc_4_datetime.hour, minutes=calc_4_datetime.minute,
                                                     seconds=calc_4_datetime.second)


                print('calc==>', calc_1)
                print('calc_2==>', calc_2)
                print('calc_3==>', calc_3)
                print('type calc_3==>', type(calc_3))
                print('calc_4==>', calc_4)
                print('calc_4_datetime==>', calc_4_datetime)
                print('calc_5==>', calc_5)
                print('calc_6', calc_6)
                print('calc_7', calc_7)
                print('type calc_6', type(calc_6))

                if calc_3 <= datetime.timedelta(hours=5):
                    time_to_end = calc_6
                    print('if time_to_end==>',time_to_end)
                else:
                    time_to_end = calc_6
                    print('else time_to_end==>', time_to_end)

                work_entry = self.env['hr.work.entry'].create({
                    'name': 'attendance',
                    'employee_id': employee_record.id,
                    'work_entry_type_id': getAtten.id,
                    'date_start': date_start_naive_after_breack,
                    'date_stop': formatted_end_hours_input if checkmax else time_to_end,
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
                        overtime_start = time_to_end
                        print('time_to_end over',time_to_end)
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
                        print("timedelta(hours=overtime_hours) ", timedelta(hours=overtime_hours))
                        overtime_start = date_stop_naive
                        overtime_stop = overtime_start + timedelta(
                            hours=overtime_hours)  # Assuming overtime duration is 8 hours
                        employee_domain = ['|', ('name', '=', employee),
                                           ('registration_number', '=', res)]
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
        else:
            raise UserError("please chose work entry type from approval type")
