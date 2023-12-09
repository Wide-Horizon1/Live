from odoo import models, fields, api
from odoo.tools import float_compare, format_date
from odoo.tools.date_utils import get_timedelta
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
                nextcall = current_level._get_next_date(allocation.employee_id.first_contract_date)
                print('next call', nextcall, leave_start_date)
                _logger.info("current_level")
                _logger.info(current_level)
                _logger.info(current_level.accrual_plan_id)
                while nextcall <= leave_start_date:
                    print('i : ', i)
                    nextcall = current_level._get_next_date(allocation.employee_id.first_contract_date)
                    print('hiiii', nextcall)
                    i += 1
                    allocation.type_from_compute = allocation.holiday_status_id
                forcasted_days = i * current_level.added_value
                print('gegege...', forcasted_days)
                _logger.info(" forcassteeed in calcuatrq3y+++++++++++++)
                _logger.info(forcasted_days)
                _logger.info(" rate in calcuatrq3y+++++++++++++)
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

