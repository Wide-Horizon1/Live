import pytz

from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_round, date_utils
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError



class HrContract(models.Model):
    _inherit = 'hr.contract'

    def _get_contract_work_entries_values(self, date_start, date_stop):
        contract_vals = super()._get_contract_work_entries_values(date_start, date_stop)
        contract_vals += self._fillGaps(date_start, date_stop)
        return contract_vals



    def _fillGaps(self, date_start, date_stop):
        contract_vals = []
        # unusaldays = holiday.employee_id._get_unusual_days(holiday.date_from, holiday.date_to)
        # for contract in self:
        #     if not contract.time_credit or not contract.time_credit_type_id:
        #         continue
        #
        #     employee = contract.employee_id
        #     resource = employee.resource_id
        #     calendar = contract.resource_calendar_id
        #     # standard_calendar = contract.standard_calendar_id
        #
        #     # YTI TODO master: The domain is hacky, but we can't modify the method signature
        #     # Add an argument compute_leaves=True on the method
        #     standard_attendances = standard_calendar._work_intervals_batch(
        #         pytz.utc.localize(date_start) if not date_start.tzinfo else date_start,
        #         pytz.utc.localize(date_stop) if not date_stop.tzinfo else date_stop,
        #         resources=resource,
        #         domain=[('resource_id', '=', -1)])[resource.id]
        #
        #     # YTI TODO master: The domain is hacky, but we can't modify the method signature
        #     # Add an argument compute_leaves=True on the method
        #     attendances = calendar._work_intervals_batch(
        #         pytz.utc.localize(date_start) if not date_start.tzinfo else date_start,
        #         pytz.utc.localize(date_stop) if not date_stop.tzinfo else date_stop,
        #         resources=resource,
        #         domain=[('resource_id', '=', -1)]
        #     )[resource.id]
        #
        #     credit_time_intervals = standard_attendances - attendances
        #
        #     for interval in credit_time_intervals:
        #         work_entry_type_id = contract.time_credit_type_id
        #         contract_vals += [{
        #             'name': "%s: %s" % (work_entry_type_id.name, employee.name),
        #             'date_start': interval[0].astimezone(pytz.utc).replace(tzinfo=None),
        #             'date_stop': interval[1].astimezone(pytz.utc).replace(tzinfo=None),
        #             'work_entry_type_id': work_entry_type_id.id,
        #             'is_credit_time': True,
        #             'employee_id': employee.id,
        #             'contract_id': contract.id,
        #             'company_id': contract.company_id.id,
        #             'state': 'draft',
        #         }]
        return contract_vals