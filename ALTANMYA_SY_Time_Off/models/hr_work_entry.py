from collections import defaultdict
from contextlib import contextmanager
from dateutil.relativedelta import relativedelta
import itertools
from psycopg2 import OperationalError

from odoo import api, fields, models, tools, _

from odoo.exceptions import ValidationError


class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    is_holiday_entry = fields.Boolean('Is holiday entry?', default=False)

    def write(self, vals):
        skip_check = not bool({'date_start', 'date_stop', 'employee_id', 'work_entry_type_id', 'active'} & vals.keys())
        if 'state' in vals:
            if vals['state'] == 'draft':
                vals['active'] = True
            elif vals['state'] == 'cancelled':
                vals['active'] = False
                skip_check &= all(self.mapped(lambda w: w.state != 'conflict'))

        if 'active' in vals:
            vals['state'] = 'draft' if vals['active'] else 'cancelled'

        with self._error_checking(skip=skip_check):
            return super(models.Model, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        start_dates = [v.get('date_from') for v in vals_list if v.get('date_from')]
        stop_dates = [v.get('date_to') for v in vals_list if v.get('date_to')]
        if any(vals.get('holiday_type', 'employee') == 'employee' and not vals.get('multi_employee',
                                                                                   False) and not vals.get(
                'employee_id', False) for vals in vals_list):
            raise ValidationError(
                _("There is no employee set on the time off. Please make sure you're logged in the correct company."))
        with self.env['hr.work.entry']._error_checking(start=min(start_dates, default=False),
                                                       stop=max(stop_dates, default=False)):
            return super(models.Model, self).create(vals_list)

    def action_confirm(self):
        start = min(self.mapped('date_from'), default=False)
        stop = max(self.mapped('date_to'), default=False)
        print('got here ', start, stop)
        with self.env['hr.work.entry']._error_checking(start=start, stop=stop):
            return super(models.Model, self).action_confirm()

    @contextmanager
    def _error_checking(self, start=None, stop=None, skip=False):
        """
        Context manager used for conflicts checking.
        When exiting the context manager, conflicts are checked
        for all work entries within a date range. By default, the start and end dates are
        computed according to `self` (min and max respectively) but it can be overwritten by providing
        other values as parameter.
        :param start: datetime to overwrite the default behaviour
        :param stop: datetime to overwrite the default behaviour
        :param skip: If True, no error checking is done
        """
        try:
            print('ULTRA ', self.env.context.get('hr_work_entry_no_check', False))
            skip = skip or self.env.context.get('hr_work_entry_no_check', False)
            start = start or min(self.mapped('date_start'), default=False)
            stop = stop or max(self.mapped('date_stop'), default=False)
            if not skip and start and stop:
                work_entries = self.sudo().with_context(hr_work_entry_no_check=True).search([
                    ('date_start', '<', stop),
                    ('date_stop', '>', start),
                    ('state', 'not in', ('validated', 'cancelled')),
                    ('is_holiday_entry', '!=', True)
                ])
                print('reseting ', work_entries)
                work_entries._reset_conflicting_state()
            yield
        except OperationalError:
            # the cursor is dead, do not attempt to use it or we will shadow the root exception
            # with a "psycopg2.InternalError: current transaction is aborted, ..."
            skip = True
            raise
        finally:
            if not skip and start and stop:
                # New work entries are handled in the create method,
                # no need to reload work entries.
                work_entries.exists()._check_if_error()