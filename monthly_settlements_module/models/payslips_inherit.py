from datetime import date
from odoo import models, api, Command
from odoo.exceptions import ValidationError
import logging

_LOGGER = logging.getLogger(__name__)


class MonthlySettlementsPaySlips(models.Model):
    _inherit = 'hr.payslip'

    @api.model_create_multi
    def create(self, vals):
        payslips = super(MonthlySettlementsPaySlips, self).create(vals)
        for payslip in payslips:
            employee = payslip.employee_id
            contract = payslip.contract_id
            print("state is ", payslip.state, contract.state)
            # Your existing logic for fetching salary slips to pay
            print("employeee is ", employee)
            salary_slips_to_pay = self.env['hr.payslip'].search([
                ("employee_id", "=", employee.id),
                ("contract_id.state", "in", ["open", "close"]),
                ("state", "in", ["verify", "draft"]),
            ])
            print("payslip is ", payslip, employee, salary_slips_to_pay)
            # Your existing logic to calculate type_totals
            # for payslip_to_pay in salary_slips_to_pay:
            mo = self.env['monthly.settlements'].search([
                ("employee_name", "=", employee.id),
                ('monthly_settlements_lines_ids.date_lines', '>=', payslip.date_from),
                ('monthly_settlements_lines_ids.date_lines', '<=', payslip.date_to),
                ('state', '=', 'done'),
            ])
            print("monthly is ", mo)
            for mo_record in mo:
                print("mo records is ", mo_record, payslip, contract)
                # for contract in payslip.contract_id:
                for lines in mo_record.monthly_settlements_lines_ids:
                    if isinstance(contract.date_start, date) and isinstance(contract.date_end, date) and isinstance(
                            lines.date_lines, date):
                        emp_will_leave = self.env['hr.employee'].search([('active', '=', False)])
                        print('Archived is -----', emp_will_leave)
                        if emp_will_leave:
                            if employee.id in emp_will_leave.ids:
                                for will_leave in emp_will_leave:
                                    print("willl leave iks ", will_leave, lines.date_lines)
                                    if will_leave.departure_date:
                                        print("$$$$$$$$$$$$$$$$$$", will_leave.departure_date)
                                        # employee = payslip.employee_id
                                        print("$$$$$$$$$$$$$$$$$$", employee)
                                        # if employee in emp_will_leave:
                                        if employee.id == will_leave.id:
                                            print(" create to this Employee leaving", employee.name, lines.delay)
                                            leave_date = will_leave.departure_date
                                            # payslip.date_from <= leave_date <= payslip.date_to:
                                            if leave_date >= payslip.date_from and leave_date <= payslip.date_to:
                                                if (
                                                        lines.date_lines >= leave_date
                                                        and contract.state == 'close'
                                                        and lines.delay == False
                                                        and leave_date == contract.date_end):
                                                    print("  خففف ")
                                                    input_line_vals = []

                                                    input_line_vals.append(Command.create({
                                                        'name': 'expired',
                                                        'amount': lines.total_amount_lines,
                                                        'input_type_id': mo_record.type.id,
                                                    }))

                                                    payslip.update({'input_line_ids': input_line_vals})
                                                    lines.status = 'expired'

                                                    print("delay is ", lines.delay, leave_date.month,
                                                          lines.date_lines.month)
                                                elif lines.date_lines <= leave_date \
                                                        and leave_date.month == lines.date_lines.month and leave_date.year == lines.date_lines.year and contract.state == 'close' and lines.delay == False:
                                                    #         and leave_date.year == lines.date_lines.year :
                                                    print("  خففففففففففففففففف ")

                                                    input_line_vals = []

                                                    input_line_vals.append(Command.create({
                                                        'name': 'expired',
                                                        'amount': lines.total_amount_lines,
                                                        'input_type_id': mo_record.type.id,
                                                    }))

                                                    payslip.update({'input_line_ids': input_line_vals})
                                                    lines.status = 'expired'
                            else:
                                print("delaaaaaaY IS $$$$$$", lines.delay, lines.status, employee.id)
                                if lines.date_lines >= payslip.date_from and lines.date_lines <= payslip.date_to and contract.date_start <= lines.date_lines <= contract.date_end and lines.delay == False:
                                    print("hello from open (()()()()()", mo_record.type.id)
                                    input_line_vals = []
                                    input_line_vals.append(Command.create({
                                        'name': lines.description_lines,
                                        'amount': lines.total_amount_lines,
                                        'input_type_id': mo_record.type.id,
                                    }))
                                    payslip.update({'input_line_ids': input_line_vals})
                                    lines.status = 'done'
                        else:
                            print("dellllllllllllllll", lines.delay, lines.date_lines, payslip.date_from,
                                  payslip.date_to, contract.state, contract.date_start, contract.date_end)
                            if lines.date_lines >= payslip.date_from and lines.date_lines <= payslip.date_to and contract.date_start <= lines.date_lines <= contract.date_end and lines.delay == False:
                                print("hello from open (()()()()()", mo_record.type.id)
                                input_line_vals = []
                                input_line_vals.append(Command.create({
                                    'name': lines.description_lines,
                                    'amount': lines.total_amount_lines,
                                    'input_type_id': mo_record.type.id,
                                }))
                                payslip.update({'input_line_ids': input_line_vals})
                                lines.status = 'done'
                                _LOGGER.info(" main account saasas")
                                _LOGGER.info(lines.status)





                    else:
                        raise ValidationError("Date of Contract doesn't set  !!!")

        return payslips
