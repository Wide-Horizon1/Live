from odoo import models, fields, api
from dateutil.parser import parse
import pytz
from pytz import timezone, utc
import base64
import xlrd

import calendar
from odoo.exceptions import UserError, ValidationError
import datetime
from xlrd.xldate import xldate_as_datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class ShowDetailsData(models.Model):
    _name = 'show.details'
    _description = 'All Details Data'

    approval_request_id = fields.Many2one('approval.request')
    employee = fields.Char(string='Employee', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    start_hour = fields.Char(string='Start Hour', readonly=True)
    end_hours = fields.Char(string='End Hours', readonly=True)
    late = fields.Char(string='Late')
    overtime = fields.Float(string='Overtime')
    apporvlelateee = fields.Boolean(default=True, string='Approval Late')
    apporvleovertime = fields.Boolean(default=True, string='Approval OverTime')


class SendData(models.Model):
    _name = 'show.data'

    approval_request_id = fields.Many2one('approval.request')
    emploey_id = fields.Char(string='id')
    name = fields.Char(string='name')
    department = fields.Char(string='department')
    working_days = fields.Char(string='working days')
    absence = fields.Integer(string='absence')
    late = fields.Char(string='late')
    overTime = fields.Char(string='overTime')
    date_from = fields.Date('From')
    date_to = fields.Date('To')


class SendData(models.Model):
    _name = 'send.data'

    approval_request_id = fields.Many2one('approval.request')
    emploey_id = fields.Char(string='id')
    name = fields.Char(string='name')
    department = fields.Char(string='department')
    working_days = fields.Char(string='working days')
    absence = fields.Integer(string='absence')
    late = fields.Char(string='late')
    overTime = fields.Char(string='overTime')

    def approved(self):
        print('sd')


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    ...

    def unlink(self):
        for request in self:
            show_data_records = self.env['show.data'].search([('approval_request_id', '=', request.id)])
            show_data_records.unlink()
            show_details_records = self.env['show.details'].search([('approval_request_id', '=', request.id)])
            show_details_records.unlink()
        return super(ApprovalRequest, self).unlink()


class AllData(models.TransientModel):
    _name = 'all.data'

    date_from = fields.Date('From')
    date_to = fields.Date('To')

    def get_data(self):
        # self.env.cr.execute('TRUNCATE send_data')
        date_from = self.date_from
        date_to = self.date_to
        print('Date From:', date_from)
        print('Date To:', date_to)
        excel_data = self.env['excel.data'].search([])
        excel_data = self.env['excel.data'].search([])
        print('excel_data==>', excel_data)
        filtered_excel_data = excel_data.filtered(
            lambda r: r.approval_request_id.request_status not in ['approved', 'pending'])

        print('filtered_excel_data', filtered_excel_data)
        sumovertime = {}
        sumlate = {}
        working_days = {}
        partner_dates = set()  # Set to store unique partner-date combinations
        filtered_data = self.env['excel.data'].browse()
        for data in filtered_excel_data:
            partner_date = (data.employee, data.date)
            if partner_date not in partner_dates:
                partner_dates.add(partner_date)
                filtered_data += data
            # Filter the data based on the selected month

        if date_from and date_to:
            filtered_data = filtered_data.filtered(lambda r: date_from <= r.date <= date_to)
        print('Filtered Data:', filtered_data)

        for data in filtered_data:
            res = data.employee.split('.')[0]  # Extract the employee ID
            if data.employee.split('.')[0].isdigit():
                employee_domain = ['|', ('name', '=', data.employee),
                                   ('registration_number', '=', res)]
                employee_record = self.env['hr.employee'].search(employee_domain, limit=1)
                name = employee_record.name
            else:
                name = data.employee
            working_days[name] = 0

        partner_dates = set()  # Set to store unique partner-date combinations
        filtered_data = self.env['excel.data'].browse()
        for data in filtered_excel_data:
            partner_date = (data.employee, data.date)
            if partner_date not in partner_dates:
                partner_dates.add(partner_date)
                filtered_data += data
        if date_from and date_to:
            filtered_data = filtered_data.filtered(lambda r: date_from <= r.date <= date_to)
        print('Filtered Data:', filtered_data)

        for data in filtered_data:

            res = data.employee.split('.')[0]  # Extract the employee ID
            if data.employee.split('.')[0].isdigit():
                employee_domain = ['|', ('name', '=', data.employee),
                                   ('registration_number', '=', res)]
                employee_record = self.env['hr.employee'].search(employee_domain, limit=1)
                name = employee_record.name
            else:
                name = data.employee
            working_days[name] += 1
            if name not in sumovertime:
                sumovertime[name] = 0.0
            if name not in sumlate:
                sumlate[name] = timedelta()

            sumovertime[name] += data.overtime

            if data.late:
                hours, minutes, seconds = data.late.split(':')
                late_duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
                sumlate[name] += late_duration

            # registration_number = employee_record.registration_number
        print('approvedapprovedapproved==>')
        approval_category = self.env['approval.category'].search([('name', '=', 'work entry')], limit=1)
        # Create the approval request
        existing_request = self.env['approval.request'].search([
            ('date_to', '>=', date_from),  # Check if existing request end date is after or on the selected start date
            ('date_from', '<=', date_to),  # Check if existing request start date is before or on the selected end date
        ], limit=1)

        print('date_from', type(date_from))
        print('date_to', type(date_to))

        print('Existing Requests:', existing_request)
        if filtered_data:
            if existing_request.request_status == 'new' or existing_request.request_status == 'pending' or existing_request.request_status == 'approved':
                # An approval request already exists for the selected date
                # You can raise an error or handle it based on your requirements
                raise ValidationError("An approval request already exists for this date")
            else:
                approval_request = self.env['approval.request'].sudo().create({
                    'name': 'New Approval Request',
                    'category_id': approval_category.id,
                    'request_owner_id': self.env.user.id,
                    'request_status': 'new',  # Set the state to approved using the correct field name
                    'date_from': date_from,  # Set the date range start
                    'date_to': date_to,  # Set the date range end

                })
                # approval_request.write({'request_status': 'approved'})
                print('approval_request..', approval_request)
                print('sumovertime==>', sumovertime)

                ###
        else:
            raise ValidationError("there are no record in this data!")

        for data in filtered_data:
            print('data==>', data)
            data.write({
                'approval_request_id': approval_request.id,
            })
            self.env['show.details'].create({
                'approval_request_id': approval_request.id,
                'employee': data.employee,
                'date': data.date,  # Replace with the appropriate field from excel_record
                'start_hour': data.start_hour,  # Replace with the appropriate field from excel_record
                'end_hours': data.end_hours,  # Replace with the appropriate field from excel_record
                'late': data.late,  # Replace with the appropriate field from excel_record
                'overtime': data.overtime,
                'apporvlelateee': data.apporvlelateee,
                'apporvleovertime': data.apporvleovertime,
            })

        for partner_id, late_duration in sumlate.items():
            total_seconds = late_duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            res = self.env['hr.employee'].search([('name', '=', partner_id)])
            registration_number = res.registration_number
            dep = res.department_id.name

            year = date_from.year  # Assuming date_from is a valid date object
            month = date_from.month
            num_days_in_month = calendar.monthrange(year, month)[1]

            # working_days = working_days[partner_id]
            absence_days = num_days_in_month - working_days[partner_id]
            print('absence_days==', absence_days)
            self.env['send.data'].create({
                'approval_request_id': approval_request.id,
                'emploey_id': registration_number,
                'name': partner_id,  # Replace with the appropriate field from excel_record
                'department': dep,  # Replace with the appropriate field from excel_record
                'working_days': working_days[partner_id],  # Replace with the appropriate field from excel_record
                'absence': absence_days,  # Replace with the appropriate field from excel_record
                'late': formatted_duration,
                'overTime': sumovertime[partner_id],
            })

            self.env['show.data'].create({
                'approval_request_id': approval_request.id,
                'emploey_id': registration_number,
                'name': partner_id,  # Replace with the appropriate field from excel_record
                'department': dep,  # Replace with the appropriate field from excel_record
                'working_days': working_days[partner_id],  # Replace with the appropriate field from excel_record
                'absence': absence_days,  # Replace with the appropriate field from excel_record
                'late': formatted_duration,
                'overTime': sumovertime[partner_id],
            })

            # for record in self:
            #     record.approval_request_id = approval_request.id
            #
            # print('approval_request..', approval_request)
        #     action = self.env.ref('ALTANMYA_EXCEL_WORKENTRY.action_get_all_data').read()[0]
        # return action
        # return approval_request
