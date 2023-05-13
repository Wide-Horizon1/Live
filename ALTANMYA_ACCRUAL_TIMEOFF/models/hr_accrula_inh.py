from odoo import api, fields, models
import logging
import pytz

from collections import namedtuple, defaultdict
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from datetime import datetime, timedelta, time
from pytz import timezone, UTC
from odoo.tools import date_utils

from odoo import api, Command, fields, models, tools
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare, format_date
from odoo.tools.float_utils import float_round
from odoo.tools.misc import format_date
from odoo.tools.translate import _
from odoo.osv import expression

_logger = logging.getLogger(__name__)

DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
# Used for displaying the days and reversing selection -> integer
DAY_SELECT_VALUES = [str(i) for i in range(1, 29)] + ['last']
DAY_SELECT_SELECTION_NO_LAST = tuple(zip(DAY_SELECT_VALUES, (str(i) for i in range(1, 29))))


class HrLeaveInh(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('state', 'number_of_days', 'holiday_status_id')
    def _check_holidays(self):
        for holiday in self:
            mapped_days = self.holiday_status_id.get_employees_days((holiday.employee_id | holiday.employee_ids).ids,
                                                                    holiday.date_from.date())
            if holiday.holiday_type != 'employee' \
                    or not holiday.employee_id and not holiday.employee_ids \
                    or holiday.holiday_status_id.requires_allocation == 'no':
                continue
            if holiday.employee_id:
                leave_days = mapped_days[holiday.employee_id.id][holiday.holiday_status_id.id]
                print('request_date_from..', holiday.request_date_from)
                print('datetime.now()...', datetime.now().date())
                print('result-data', holiday.request_date_from - datetime.now().date())
                print('leave_days..', leave_days)
                print("float_compare(leave_days['remaining_leaves'], 0, precision_digits=2)..",
                      float_compare(leave_days['remaining_leaves'], 0, precision_digits=2))
                print("float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2)",
                      float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2))
                allocation = self.env['hr.leave.allocation'].search([('employee_id', '=', holiday.employee_id.id),
                                                                     ('allocation_type', '=', 'accrual')])
                print('alllocasnvisdnv ', allocation)
                m = allocation.get_total_invoked(holiday.request_date_from)
                print('tetetst..',m)
                if float_compare(leave_days['remaining_leaves'], 0, precision_digits=2) == -1 \
                        or float_compare(leave_days['virtual_remaining_leaves'] + m, 0, precision_digits=2) == -1:
                    print('sadads',float_compare(leave_days['virtual_remaining_leaves'] + m, 0, precision_digits=2))
                    raise ValidationError(
                        _('The number of remaining time off is not sufficient for this time off type.\n'
                          'Please also check the time off waiting for validation.'))
            else:
                unallocated_employees = []
                for employee in holiday.employee_ids:
                    leave_days = mapped_days[employee.id][holiday.holiday_status_id.id]
                    if float_compare(leave_days['remaining_leaves'], self.number_of_days, precision_digits=2) == -1 \
                            or float_compare(leave_days['virtual_remaining_leaves'], self.number_of_days,
                                             precision_digits=2) == -1:
                        unallocated_employees.append(employee.name)
                if unallocated_employees:
                    raise ValidationError(
                        _('The number of remaining time off is not sufficient for this time off type.\n'
                          'Please also check the time off waiting for validation.')
                        + _('\nThe employees that lack allocation days are:\n%s',
                            (', '.join(unallocated_employees))))


class test(models.Model):
    _inherit = 'hr.leave.allocation'

    def get_total_invoked(self, leave_start_date):
        for allocation in self:
            i = 1
            (current_level, current_level_idx) = allocation._get_current_accrual_plan_level_id(allocation.nextcall)
            print('allocation : ', allocation, allocation.nextcall)
            forcasted_days = 0
            if current_level:
                nextcall = current_level._get_next_date(allocation.nextcall)
                print('next call', nextcall , leave_start_date)
                while nextcall <= leave_start_date:
                    print('i : ', i)
                    nextcall = current_level._get_next_date(nextcall)
                    print('hiiii', nextcall)
                    i += 1
                forcasted_days = i * current_level.added_value
        return forcasted_days

            # if self._get_next_date_edited(self.last)


class AcoHrLeaveInh(models.Model):
    _inherit = 'hr.leave.accrual.level'

    def _get_next_date_edited(self, last_call):
        """
        Returns the next date with the given last call
        """

        self.ensure_one()
        if self.frequency == 'daily':
            return last_call + relativedelta(days=1)
        elif self.frequency == 'weekly':
            daynames = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            weekday = daynames.index(self.week_day)
            return last_call + relativedelta(days=1, weekday=weekday)
        elif self.frequency == 'bimonthly':
            first_date = last_call + relativedelta(day=self.first_day)
            second_date = last_call + relativedelta(day=self.second_day)
            if last_call < first_date:
                return first_date
            elif last_call < second_date:
                return second_date
            else:
                return last_call + relativedelta(months=1, day=self.first_day)
        elif self.frequency == 'monthly':
            date = last_call + relativedelta(day=self.first_day)
            if last_call < date:
                return date
            else:
                return last_call + relativedelta(months=1, day=self.first_day)
        elif self.frequency == 'biyearly':
            first_month = MONTHS.index(self.first_month) + 1
            second_month = MONTHS.index(self.second_month) + 1
            first_date = last_call + relativedelta(month=first_month, day=self.first_month_day)
            second_date = last_call + relativedelta(month=second_month, day=self.second_month_day)
            if last_call < first_date:
                return first_date
            elif last_call < second_date:
                return second_date
            else:
                return last_call + relativedelta(years=1, month=first_month, day=self.first_month_day)
        elif self.frequency == 'yearly':
            month = MONTHS.index(self.yearly_month) + 1
            date = last_call + relativedelta(month=month, day=self.yearly_day)
            if last_call < date:
                return date
            else:
                return last_call + relativedelta(years=1, month=month, day=self.yearly_day)
        else:
            return False
