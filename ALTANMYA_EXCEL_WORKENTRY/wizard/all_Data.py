from odoo import models, fields, api
from dateutil.parser import parse
import pytz
from pytz import timezone, utc
import base64
import xlrd
from odoo.exceptions import UserError, ValidationError
import datetime
from xlrd.xldate import xldate_as_datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class SendData(models.Model):
    _name = 'send.data'

    approval_request_id = fields.Many2one('approval.request')
    emploey_id = fields.Char(string='id')
    name = fields.Char(string='name')
    department = fields.Char(string='department')
    working_days = fields.Char(string='working days')
    absence = fields.Char(string='absence')
    late = fields.Char(string='late')
    overTime = fields.Char(string='overTime')

    def approved(self):
        print('sd')


class AllData(models.TransientModel):
    _name = 'all.data'

    date_from = fields.Date('From')
    date_to = fields.Date('To')

    def get_data(self):
        self.env.cr.execute('TRUNCATE send_data')
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
        ])

        print('date_from',type(date_from))
        print('date_to',type(date_to))

        if filtered_data:
            print('Existing Requests:', existing_request)
            if existing_request:
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
            data.write({
                'approval_request_id': approval_request.id,
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

            self.env['send.data'].create({
                'approval_request_id': approval_request.id,
                'emploey_id': registration_number,
                'name': partner_id,  # Replace with the appropriate field from excel_record
                'department': dep,  # Replace with the appropriate field from excel_record
                'working_days': working_days[partner_id],  # Replace with the appropriate field from excel_record
                'absence': '0323',  # Replace with the appropriate field from excel_record
                'late': formatted_duration,
                'overTime': sumovertime[partner_id],
            })

            # for record in self:
            #     record.approval_request_id = approval_request.id
            #
            # print('approval_request..', approval_request)

        # return approval_request
