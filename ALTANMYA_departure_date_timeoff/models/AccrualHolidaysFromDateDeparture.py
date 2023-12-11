from odoo import models, fields, api
from odoo.tools import float_compare, format_date
from datetime import datetime, timedelta, time


import logging


_logger = logging.getLogger(__name__)



class AccrualHolidaysFromDateDeparture(models.Model):
    _inherit = 'hr.employee'

    all_allocation_for_this_emp = fields.Char('All Allocations', readonly=True, compute='all_allocations')
    all_time_off_for_this_emp = fields.Char('All Time Off', readonly=True, compute='all_time_off')
    remaining_time_off = fields.Text('Remaining Time Off', readonly=True, compute='calc_remaining_time_off')
    total_remaining_time_off = fields.Float('Total Remaining Time Off', readonly=True,
                                            compute='calc_total_remaining_time_off')
    possible_days = fields.Char('Total Days', readonly=True, compute='_get_date_possible', default="")
    days_help_field = fields.Float('days help field')

    balance = fields.Float('Balance', readonly=True,
                                            compute='calc_balance')

    @api.depends('active')
    # @api.onchange('request_date_from')
    def _get_date_possible(self):
        print("archiveddddddddd")
        self.possible_days = 0.0
        total_remaining_leaves = 0.0
        for employee in self:
            print("archive", employee.departure_date)
            # employee.possible_days = 0

            if employee.departure_date:
                print("hello here ")
                all_allocations = self.env['hr.leave.allocation'].search(
                    [('employee_id', '=', employee.id), ('active', 'in', [False, True]), ('state', '=', 'validate'),
                     ('allocation_type', '=', 'accrual')])
                print("allocation is ", all_allocations)
                _logger.info("  all allocations  in calc +++++++++++++")
                _logger.info(all_allocations)
                for allocation in all_allocations:
                    employee.possible_days = 0.0
                    if allocation.holiday_status_id:
                        # aco_hr_leave = allocation.holiday_status_id.Forecast_Future_Allocation
                        # print('b6e511115 111..', allocation.holiday_status_id.Forecast_Future_Allocation)
                        # if aco_hr_leave:
                        # Perform the necessary computations
                        mapped_days = allocation.holiday_status_id.get_employees_days(
                            (allocation.employee_id | allocation.employee_id).ids,
                            employee.departure_date)
                        _logger.info("  mapped days in calc +++++++++++++")
                        _logger.info(mapped_days)
                        _logger.info( allocation.holiday_status_id)
                        _logger.info(allocation.employee_id)
                        _logger.info(allocation.employee_ids)
                        _logger.info((allocation.employee_id | allocation.employee_id).ids)
                        _logger.info(employee.departure_date)
                        if allocation.holiday_type != 'employee' \
                                or not allocation.employee_id \
                                or allocation.holiday_status_id.requires_allocation == 'no':
                            continue
                            print('continueseeee', allocation.employee_id)
                        if allocation.employee_id:
                            print('inside......', allocation.employee_id)
                            leave_days = mapped_days[allocation.employee_id.id][allocation.holiday_status_id.id]
                            # allocation = self.env['hr.leave.allocation'].search(
                            #     [('employee_id', '=', allocation.employee_id.id),
                            #      ('allocation_type', '=', 'accrual')])
                            print("lllllllllll", leave_days)
                            total_remaining_leaves += leave_days['virtual_remaining_leaves']
                            m = allocation.get_total_days(employee.departure_date)
                            print("mmmmmmmmmmmm", m)
                            _logger.info("  mmmmmmm in calc +++++++++++++")
                            _logger.info(m)
                            _logger.info("  virtual_remaining_leaves in calc +++++++++++++")
                            _logger.info(leave_days['virtual_remaining_leaves'])

                            employee.possible_days = m + total_remaining_leaves
                            print('self.possible_days..', employee.possible_days)
                            print("leave_days['virtual_remaining_leaves']", leave_days['virtual_remaining_leaves'])
                            print('mvvv.m..', m)
                    # else:
                    #     # Set possible_days to a default value when Forecast_Future_Allocation is False
                    #     mapped_days = self.holiday_status_id.get_employees_days(
                    #         (holiday.employee_id | holiday.employee_ids).ids,
                    #         holiday.date_from.date())
                    #     if holiday.holiday_type != 'employee' \
                    #             or not holiday.employee_id and not holiday.employee_ids \
                    #             or holiday.holiday_status_id.requires_allocation == 'no':
                    #         continue
                    #     print('holiday.employee_id.outsiad2..', holiday.employee_id)
                    #     if holiday.employee_id:
                    #         print('holiday.employee_id.outsiad33..', holiday.employee_id, mapped_days)
                    #         leave_days = mapped_days[holiday.employee_id.id][holiday.holiday_status_id.id]
                    #         print('leave_daysasd..', leave_days)
                    #         allocation = self.env['hr.leave.allocation'].search(
                    #             [('employee_id', '=', holiday.employee_id.id),
                    #              ('allocation_type', '=', 'accrual')])
                    #         m = allocation.get_total_invoked(holiday.request_date_from)
                    #
                    #         holiday.possible_days = leave_days['virtual_remaining_leaves']
                    #         print('self.possible_days..', holiday.possible_days)
                    #         print("leave_days['virtual_remaining_leaves']", leave_days['virtual_remaining_leaves'])
                    #         print('mvvv.m..', m)
                    else:
                        print("ssssssss"
                              )
                        employee.possible_days = 0.0

    @api.depends('active')
    def all_allocations(self):
        for rec in self:
            text = ''
            total_days = 0
            holiday_status = self.env['hr.leave.type'].search([('requires_allocation', '=', 'yes')])
            for t in holiday_status:
                all_allocations = self.env['hr.leave.allocation'].search(
                    [('employee_id', '=', rec.id), ('active', 'in', [False, True]), ('state', '=', 'validate'),
                     ('holiday_status_id', '=', t.id)])
                leave_type_days = sum(allocation.number_of_days_display for allocation in all_allocations)
                if leave_type_days > 0:
                    text += str(('%s duration %s,' % (t.name, leave_type_days)))
                    total_days += leave_type_days
            if total_days > 0:
                text = f'Total = {total_days}, Details = {text}'
            else:
                text = "No Records"
            rec.all_allocation_for_this_emp = text

    @api.depends('active')
    def all_time_off(self):
        for rec in self:
            rec.all_time_off_for_this_emp = ''
            accrual_type = self.env['hr.leave.allocation'].search(
                [('employee_id', '=', rec.id), ('allocation_type', '=', 'accrual'),('active', 'in', [False , True])])
            for acc in accrual_type:
                if acc.type_from_compute:
                    all_time_off = self.env['hr.leave'].search(
                        [('employee_id', '=', rec.id), ('state', '=', 'validate'),
                         ('holiday_status_id', '=', acc.type_from_compute.id)])
                    rec.all_time_off_for_this_emp = ''
                    print('11111111111111')
                    if all_time_off:
                        total_days = 0
                        for time_off in all_time_off:
                            print('222222222222')
                            total_days += time_off.number_of_days_display
                            rec.days_help_field = total_days
                            text = str(
                                ('%s duration %s,' % (time_off.holiday_status_id.name, total_days)))
                            rec.all_time_off_for_this_emp = str(text)
                            print('textttttt', text)
                    else:
                        print('33333333333')
                        text = "No Records"
                        rec.all_time_off_for_this_emp = str(text)
                else:
                    print('33333333333')
                    text = "No Records"
                    rec.all_time_off_for_this_emp = str(text)

    @api.depends('active')
    def calc_remaining_time_off(self):
        for rec in self:
            text = 'Remaining: '
            holiday_status = self.env['hr.leave.type'].search([('requires_allocation', '=', 'yes')])
            for t in holiday_status:
                used = self.env['hr.leave'].search([
                    ('employee_id', '=', rec.id),
                    ('holiday_status_id', '=', t.id),
                    ('state', '=', 'validate')
                ])
                has = self.env['hr.leave.allocation'].search([
                    ('employee_id', '=', rec.id),
                    ('holiday_status_id', '=', t.id),
                    ('active', 'in', [False]),
                    ('state', '=', 'validate')
                ])
                if used or has:
                    remaining_days = has.number_of_days_display - used.number_of_days_display
                    text += str(('%s duration %s,' % (t.name, str(remaining_days))))

            if rec.all_allocation_for_this_emp == rec.all_time_off_for_this_emp == "No Records":
                text = "No Records"
            rec.remaining_time_off = str(text)

    @api.depends('possible_days')
    def calc_balance(self):
        for rec in self :

            if rec.departure_date:
                total = float(rec.possible_days) - rec.days_help_field
                rec.balance = total
            else:
                rec.balance = 0.0


    """
    date_to : departure date , and didnt work with user
    100     365 
    x        39

    """
