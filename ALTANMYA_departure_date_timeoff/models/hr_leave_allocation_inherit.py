from collections import defaultdict

from odoo import models, fields, api
from odoo.tools import float_compare, format_date
from odoo.tools.date_utils import get_timedelta
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools import format_date
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round
from datetime import time, timedelta

from odoo.addons.resource.models.resource import Intervals

import logging


_logger = logging.getLogger(__name__)


class Hrleaveallocation(models.Model):
    _inherit = 'hr.leave.allocation'

    type_from_compute= fields.Many2one('hr.leave.type')

    def get_total_days(self, leave_start_date):
        forcasted_days = 0
        for allocation in self:
            i = 0
            (current_level, current_level_idx) = allocation._get_current_accrual_plan_level_id(allocation.nextcall)
            print('allocation : ', allocation, allocation.employee_id.first_contract_date)
            forcasted_days = 0
            if current_level:
                print('current level : ', current_level.accrual_plan_id, current_level_idx)
                print("i am here ")
                nextcall = current_level._get_next_date(allocation.nextcall)
                print('next call', nextcall, leave_start_date)
                _logger.info("current_level")
                _logger.info(nextcall)
                _logger.info(current_level)
                _logger.info(current_level.accrual_plan_id)
                while nextcall <= leave_start_date:
                    print('i : ', i)
                    nextcall = current_level._get_next_date(nextcall)
                    print('hiiii', nextcall)
                    i += 1
                    allocation.type_from_compute = allocation.holiday_status_id
                forcasted_days = i * current_level.added_value
                print('gegege...', forcasted_days)
                _logger.info(" forcassteeed in calcuatrq3y+++++++++++++")
                _logger.info(forcasted_days)
                _logger.info(" rate in calcuatrq3y+++++++++++++")
                _logger.info(current_level.added_value)
                print('geg22ege...', current_level.added_value)
                
        return forcasted_days

        # if self._get_next_date_edited(self.last)

    def _get_current_accrual_plan_level_id(self, date, level_ids=False):
        """
        Returns a pair (accrual_plan_level, idx) where accrual_plan_level is the level for the given date
         and idx is the index for the plan in the ordered set of levels
        """
        self.ensure_one()
        if not self.accrual_plan_id.level_ids:
            return (False, False)
        # Sort by sequence which should be equivalent to the level
        if not level_ids:
            level_ids = self.accrual_plan_id.level_ids.sorted('sequence')
        current_level = False
        current_level_idx = -1
        for idx, level in enumerate(level_ids):
            if date:
                if date > self.date_from + get_timedelta(level.start_count, level.start_type):
                    current_level = level
                    current_level_idx = idx
        # If transition_mode is set to `immediately` or we are currently on the first level
        # the current_level is simply the first level in the list.
        if current_level_idx <= 0 or self.accrual_plan_id.transition_mode == "immediately":
            return (current_level, current_level_idx)
        # In this case we have to verify that the 'previous level' is not the current one due to `end_of_accrual`
        level_start_date = self.date_from + get_timedelta(current_level.start_count, current_level.start_type)
        previous_level = level_ids[current_level_idx - 1]
        # If the next date from the current level's start date is before the last call of the previous level
        # return the previous level
        if current_level._get_next_date(level_start_date) < previous_level._get_next_date(level_start_date):
            return (previous_level, current_level_idx - 1)
        return (current_level, current_level_idx)
        
class HrLeavetype(models.Model) :
    _inherit = 'hr.leave.type'

    def _get_employees_days_per_allocation(self, employee_ids, date=None):
        print("88888888888888888` ", employee_ids)
        print("9999999999999999999` ", self.ids)
        leaves = self.env['hr.leave'].search([
            ('employee_id', 'in', employee_ids),
            ('state', 'in', ['confirm', 'validate1', 'validate']),
            ('holiday_status_id', 'in', self.ids)
        ])
        print("leaaaaaaaave ", leaves)
        allocations = self.env['hr.leave.allocation'].with_context(active_test=False).search([
            ('employee_id', 'in', employee_ids),
            ('state', 'in', ['validate']),
            ('holiday_status_id', 'in', self.ids),
        ])
        print("allocations 000000000000000000000000", allocations)
        if not date:
            date = fields.Date.to_date(self.env.context.get('default_date_from')) or fields.Date.context_today(self)
        # The allocation_employees dictionary groups the allocations based on the employee and the holiday type
        # The structure is the following:
        # - KEYS:
        # allocation_employees
        #   |--employee_id
        #      |--holiday_status_id
        # - VALUES:
        # Intervals with the start and end date of each allocation and associated allocations within this interval
        allocation_employees = defaultdict(lambda: defaultdict(list))
        ### Creation of the allocation intervals ###
        for holiday_status_id in allocations.holiday_status_id:
            for employee_id in employee_ids:
                allocation_intervals = Intervals([(
                    fields.datetime.combine(allocation.date_from, time.min),
                    fields.datetime.combine(allocation.date_to or datetime.date.max, time.max),
                    allocation)
                    for allocation in allocations.filtered(lambda
                                                               allocation: allocation.employee_id.id == employee_id and allocation.holiday_status_id == holiday_status_id)])
                allocation_employees[employee_id][holiday_status_id] = allocation_intervals

        # The leave_employees dictionary groups the leavess based on the employee and the holiday type
        # The structure is the following:
        # - KEYS:
        # leave_employees
        #   |--employee_id
        #      |--holiday_status_id
        # - VALUES:
        # Intervals with the start and end date of each leave and associated leave within this interval
        leaves_employees = defaultdict(lambda: defaultdict(list))
        leave_intervals = []
        ### Creation of the leave intervals ###
        if leaves:
            for holiday_status_id in leaves.holiday_status_id:
                for employee_id in employee_ids:
                    leave_intervals = Intervals([(
                        fields.datetime.combine(leave.date_from, time.min),
                        fields.datetime.combine(leave.date_to, time.max),
                        leave)
                        for leave in leaves.filtered(lambda
                                                         leave: leave.employee_id.id == employee_id and leave.holiday_status_id == holiday_status_id)])

                    leaves_employees[employee_id][holiday_status_id] = leave_intervals

        # allocation_days_consumed is a dictionary to map the number of days/hours of leaves taken per allocation
        # The structure is the following:
        # - KEYS:
        # allocation_days_consumed
        #  |--employee_id
        #      |--holiday_status_id
        #          |--allocation
        #              |--virtual_leaves_taken
        #              |--leaves_taken
        #              |--virtual_remaining_leaves
        #              |--remaining_leaves
        #              |--max_leaves
        #              |--closest_allocation_to_expire
        # - VALUES:
        # Integer representing the number of (virtual) remaining leaves, (virtual) leaves taken or max leaves for each allocation.
        # The unit is in hour or days depending on the leave type request unit
        allocations_days_consumed = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0))))

        company_domain = [
            ('company_id', 'in', list(set(self.env.company.ids + self.env.context.get('allowed_company_ids', []))))]
        ### Existing leaves assigned to allocations ###
        if leaves_employees:
            for employee_id, leaves_interval_by_status in leaves_employees.items():
                for holiday_status_id in leaves_interval_by_status:
                    days_consumed = allocations_days_consumed[employee_id][holiday_status_id]
                    if allocation_employees[employee_id][holiday_status_id]:
                        allocations = allocation_employees[employee_id][holiday_status_id] & leaves_interval_by_status[
                            holiday_status_id]
                        available_allocations = self.env['hr.leave.allocation']
                        for allocation_interval in allocations._items:
                            available_allocations |= allocation_interval[2]
                        # Consume the allocations that are close to expiration first
                        sorted_available_allocations = available_allocations.filtered('date_to').sorted(key='date_to')
                        sorted_available_allocations += available_allocations.filtered(
                            lambda allocation: not allocation.date_to)
                        leave_intervals = leaves_interval_by_status[holiday_status_id]._items
                        sorted_allocations_with_remaining_leaves = self.env['hr.leave.allocation']
                        for leave_interval in leave_intervals:
                            leaves = leave_interval[2]
                            for leave in leaves:
                                if leave.leave_type_request_unit in ['day', 'half_day']:
                                    leave_duration = leave.number_of_days
                                    leave_unit = 'days'
                                else:
                                    leave_duration = leave.number_of_hours_display
                                    leave_unit = 'hours'
                                if holiday_status_id.requires_allocation != 'no':
                                    for available_allocation in sorted_available_allocations:
                                        if available_allocation.date_to and available_allocation.date_to < leave.date_from.date():
                                            continue
                                        virtual_remaining_leaves = (
                                                                       available_allocation.number_of_days if leave_unit == 'days' else available_allocation.number_of_hours_display) - \
                                                                   allocations_days_consumed[employee_id][
                                                                       holiday_status_id][available_allocation][
                                                                       'virtual_leaves_taken']
                                        max_leaves = min(virtual_remaining_leaves, leave_duration)
                                        days_consumed[available_allocation]['virtual_leaves_taken'] += max_leaves
                                        if leave.state == 'validate':
                                            days_consumed[available_allocation]['leaves_taken'] += max_leaves
                                        leave_duration -= max_leaves
                                        # Check valid allocations with still availabe leaves on it
                                        if days_consumed[available_allocation][
                                            'virtual_remaining_leaves'] > 0 and available_allocation.date_to and available_allocation.date_to > date:
                                            sorted_allocations_with_remaining_leaves |= available_allocation
                                    if leave_duration > 0:
                                        # There are not enough allocation for the number of leaves
                                        days_consumed[False]['virtual_remaining_leaves'] -= leave_duration
                                else:
                                    days_consumed[False]['virtual_leaves_taken'] += leave_duration
                                    if leave.state == 'validate':
                                        days_consumed[False]['leaves_taken'] += leave_duration
                        # no need to sort the allocations again
                        allocations_days_consumed[employee_id][holiday_status_id][False][
                            'closest_allocation_to_expire'] = sorted_allocations_with_remaining_leaves[
                            0] if sorted_allocations_with_remaining_leaves else False

        # Future available leaves
        for employee_id, allocation_intervals_by_status in allocation_employees.items():
            for holiday_status_id, intervals in allocation_intervals_by_status.items():
                print(")000000000000000000000000000000000000000000000", intervals, holiday_status_id)
                if not intervals:
                    continue
                future_allocation_intervals = intervals & Intervals([(
                    fields.datetime.combine(date, time.min),
                    fields.datetime.combine(date, time.max) + timedelta(days=5 * 365),
                    self.env['hr.leave'])])
                search_date = date
                closest_allocations = self.env['hr.leave.allocation']
                for interval in intervals._items:
                    closest_allocations |= interval[2]
                allocations_with_remaining_leaves = self.env['hr.leave.allocation']
                for future_allocation_interval in future_allocation_intervals._items:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    if future_allocation_interval[0].date() > search_date:
                        continue
                    for allocation in future_allocation_interval[2]:
                        print("****************************************************",
                              allocations_days_consumed[employee_id][holiday_status_id][allocation])

                        if not allocation.active:
                            print("ffffffffffffffffffff2 _______________________________________")
                            print("ooooooooooooooooooooooooooooooo _______________________________________")
                            days_consumed = allocations_days_consumed[employee_id][holiday_status_id][allocation]
                            print("DAY CONSUMED : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", days_consumed)
                            if future_allocation_interval[1] != fields.datetime.combine(date, time.max) + timedelta(
                                    days=5 * 365):
                                # Compute the remaining number of days/hours in the allocation only if it has an end date
                                quantity_available = allocation.employee_id._get_work_days_data_batch(
                                    future_allocation_interval[0],
                                    future_allocation_interval[1],
                                    compute_leaves=False,
                                    domain=company_domain)[employee_id]
                            else:
                                # If no end date to the allocation, consider the number of days remaining as infinite
                                quantity_available = {'days': float('inf'), 'hours': float('inf')}
                            if allocation.type_request_unit in ['day', 'half_day']:
                                print("hhhhhhhhhhhhhhhhhhhhhhh _______________________________________")

                                quantity_available = quantity_available['days']
                                remaining_days_allocation = (
                                        allocation.number_of_days - days_consumed['virtual_leaves_taken'])
                            else:
                                quantity_available = quantity_available['hours']
                                remaining_days_allocation = (
                                        allocation.number_of_hours_display - days_consumed['virtual_leaves_taken'])
                            if quantity_available <= remaining_days_allocation:
                                print("tttttttttttttttt _______________________________________")

                                search_date = future_allocation_interval[1].date() + timedelta(days=1)
                            print("befoooore _______________________________________",
                                  days_consumed['virtual_remaining_leaves'], days_consumed['max_leaves'],
                                  days_consumed['remaining_leaves'])
                            days_consumed['virtual_remaining_leaves'] += min(quantity_available,
                                                                             remaining_days_allocation)
                            days_consumed['max_leaves'] = allocation.number_of_days if allocation.type_request_unit in [
                                'day', 'half_day'] else allocation.number_of_hours_display
                            days_consumed['remaining_leaves'] = days_consumed['max_leaves'] - days_consumed[
                                'leaves_taken']
                            print("after _______________________________________",
                                  days_consumed['virtual_remaining_leaves'], days_consumed['max_leaves'],
                                  days_consumed['remaining_leaves'])

                            if remaining_days_allocation >= quantity_available:
                                break
                            # Check valid allocations with still availabe leaves on it
                            if days_consumed[
                                'virtual_remaining_leaves'] > 0 and allocation.date_to and allocation.date_to > date:
                                allocations_with_remaining_leaves |= allocation
                            continue
                        print("DAY CONSUMEDdddddddddddddddd : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                        days_consumed = allocations_days_consumed[employee_id][holiday_status_id][allocation]
                        print("DAY CONSUMED : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", days_consumed)
                        if future_allocation_interval[1] != fields.datetime.combine(date, time.max) + timedelta(
                                days=5 * 365):
                            # Compute the remaining number of days/hours in the allocation only if it has an end date
                            quantity_available = allocation.employee_id._get_work_days_data_batch(
                                future_allocation_interval[0],
                                future_allocation_interval[1],
                                compute_leaves=False,
                                domain=company_domain)[employee_id]
                        else:
                            # If no end date to the allocation, consider the number of days remaining as infinite
                            quantity_available = {'days': float('inf'), 'hours': float('inf')}
                        if allocation.type_request_unit in ['day', 'half_day']:
                            print("hhhhhhhhhhhhhhhhhhhhhhh _______________________________________")

                            quantity_available = quantity_available['days']
                            remaining_days_allocation = (
                                        allocation.number_of_days - days_consumed['virtual_leaves_taken'])
                        else:
                            quantity_available = quantity_available['hours']
                            remaining_days_allocation = (
                                        allocation.number_of_hours_display - days_consumed['virtual_leaves_taken'])
                        if quantity_available <= remaining_days_allocation:
                            print("tttttttttttttttt _______________________________________")

                            search_date = future_allocation_interval[1].date() + timedelta(days=1)
                        print("befoooore _______________________________________",
                              days_consumed['virtual_remaining_leaves'], days_consumed['max_leaves'],
                              days_consumed['remaining_leaves'])
                        days_consumed['virtual_remaining_leaves'] += min(quantity_available, remaining_days_allocation)
                        days_consumed['max_leaves'] = allocation.number_of_days if allocation.type_request_unit in [
                            'day', 'half_day'] else allocation.number_of_hours_display
                        days_consumed['remaining_leaves'] = days_consumed['max_leaves'] - days_consumed['leaves_taken']
                        print("after _______________________________________",
                              days_consumed['virtual_remaining_leaves'], days_consumed['max_leaves'],
                              days_consumed['remaining_leaves'])

                        if remaining_days_allocation >= quantity_available:
                            break
                        # Check valid allocations with still availabe leaves on it
                        if days_consumed[
                            'virtual_remaining_leaves'] > 0 and allocation.date_to and allocation.date_to > date:
                            allocations_with_remaining_leaves |= allocation
                allocations_sorted = sorted(allocations_with_remaining_leaves, key=lambda a: a.date_to)
                allocations_days_consumed[employee_id][holiday_status_id][False]['closest_allocation_to_expire'] = \
                allocations_sorted[0] if allocations_sorted else False
                print(" dddddddddd  ", allocations_days_consumed)
        return allocations_days_consumed



