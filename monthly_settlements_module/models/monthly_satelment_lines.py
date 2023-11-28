from odoo import fields, models, api, _

from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class MonthlySettlementsLines(models.Model):
    _name = "monthly.settlements.lines"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = "Monthly Settlements Lines Sys"

    total_from_payslip = fields.Float(string='Total from Payslip', tracking=True)
    date_lines = fields.Date(string='Date Of Settlement', tracking=True)
    description_lines = fields.Char(string='Description', tracking=True)
    total_amount_lines = fields.Float(string='Total Amount Lines', tracking=True)
    monthly_settlements_lines_id = fields.Many2one('monthly.settlements', string="Monthly Settlements Lines",
                                                   tracking=True)
    delay = fields.Boolean(string="Delay", tracking=True)
    is_changed = fields.Boolean(string="ischanged", tracking=True)
    status = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('expired', 'Expired'),
        ('delayed', 'Delayed'),
    ], default='draft', tracking=True )

    def delay_reload_action(self):
        last_record = self.env['monthly.settlements.lines'].search([
            ('monthly_settlements_lines_id', '=', self.monthly_settlements_lines_id.ids)
        ], order='date_lines desc', limit=1)
        next_date = fields.Date.from_string(last_record.date_lines) + relativedelta(months=1)
        next_date_str = fields.Date.to_string(next_date)
        self.env['monthly.settlements.lines'].create({
            'date_lines': next_date_str,
            'description_lines': self.description_lines,
            'total_amount_lines': self.total_amount_lines,
            'monthly_settlements_lines_id': self.monthly_settlements_lines_id.id,
            # 'delay': False,
        })
        self.delay = True

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def write(self, vals):
        date_total = ('date_lines' in vals and self.date_lines != vals['date_lines']) or (
                'total_amount_lines' in vals and self.total_amount_lines != vals['total_amount_lines'])
        delay_description = ('delay' in vals and self.delay != vals['delay']) or (
                'description_lines' in vals and self.description_lines != vals['description_lines'])
        if date_total or delay_description:
            if 'date_lines' in vals and self.date_lines != vals['date_lines']:
                prev_date = self.date_lines
                last_editing_date = vals['date_lines']
            else:
                prev_date = self.date_lines
                last_editing_date = self.date_lines

            if 'total_amount_lines' in vals and self.total_amount_lines != vals['total_amount_lines']:
                prev_amount = self.total_amount_lines
                last_editing_amount = vals['total_amount_lines']
            else:
                prev_amount = self.total_amount_lines
                last_editing_amount = self.total_amount_lines
            if 'delay' in vals and self.delay != vals['delay']:
                prev_delay = self.delay
                last_editing_delay = vals['delay']
            else:
                prev_delay = self.delay
                last_editing_delay = self.delay

            if 'description_lines' in vals and self.description_lines != vals['description_lines']:
                prev_description_lines = self.description_lines
                last_editing_description_lines = vals['description_lines']
            else:
                prev_description_lines = self.description_lines
                last_editing_description_lines = self.description_lines

            get_all_line_number = self.env['monthly.settlements.lines'].search([
                ('monthly_settlements_lines_id', '=', self.monthly_settlements_lines_id.id)
            ])
            line_updated = False
            if self.monthly_settlements_lines_id:
                for get_specific_line_number in get_all_line_number:
                    line_date = get_specific_line_number.date_lines
                    line_amount = get_specific_line_number.total_amount_lines
                    line_delay = get_specific_line_number.delay
                    line_description_lines = get_specific_line_number.description_lines
                    if (
                            (line_date != prev_date and line_date != last_editing_date) or
                            (line_amount != prev_amount and line_amount != last_editing_amount) or
                            (line_delay != prev_delay and line_delay != last_editing_delay) or
                            (
                                    line_description_lines != prev_description_lines and line_description_lines != last_editing_description_lines)
                    ):
                        all_lines_in_one = self.monthly_settlements_lines_id.monthly_settlements_lines_ids
                        index = 1
                        line_number = 1
                        for target_line in all_lines_in_one:
                            if target_line.id == self.id:
                                line_number = index
                            index += 1
                        line_updated = True
                        break

                if line_updated:
                    messages = []
                    if 'delay' in vals:
                        messages.append(f"We have delay in line {line_number}")
                    if 'date_lines' in vals:
                        messages.append(
                            f"We have edite in date from {prev_date} to {last_editing_date} in line {line_number}")
                    if 'total_amount_lines' in vals:
                        messages.append(
                            f"We have edite amount from {prev_amount} to {last_editing_amount} in line {line_number}")
                    if 'description_lines' in vals:
                        messages.append(
                            f"We have edite description from {prev_description_lines} to {last_editing_description_lines} in line {line_number}")
                    if messages:
                        full_message = " , ".join(messages)
                        self.monthly_settlements_lines_id.message_post(body=full_message)
                        super(MonthlySettlementsLines, self).write(vals)
        else:
            super(MonthlySettlementsLines, self).write(vals)

