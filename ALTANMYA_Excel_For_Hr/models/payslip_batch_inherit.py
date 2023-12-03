from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging

_LOGGER = logging.getLogger(__name__)

class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    emp_name=fields.Char(related='employee_id.name')
    emp_id=fields.Char(related='employee_id.identification_id')
    house_wage=fields.Float(compute='_compute_net')
    allowances=fields.Float(compute='_compute_net')
    deductions =fields.Float(compute='_compute_net')
    mobile_allowance =fields.Float(compute='_compute_net',default=0.0)
    transportation_allowance =fields.Float(compute='_compute_net',default=0.0)
    food_allowance =fields.Float(compute='_compute_net',default=0.0)
    nature_of_work=fields.Float(compute='_compute_net',default=0.0)
    total_allowances=fields.Float(compute='_compute_net',default=0.0)
    other_allowances =fields.Float(compute='_compute_net',default=0.0)
    busniess_trip =fields.Float(compute='_compute_net',default=0.0)
    worked_days= fields.Float(string = "worked days" , compute='_compute_days',default=0.0)
    basic_sal = fields.Float(string = "Baseic days" , compute='_compute_net',default=0.0)
    rewards = fields.Float(string = "Rewards " , compute='_compute_net',default=0.0)
    retrived = fields.Float(string = "Retrived " , compute='_compute_net',default=0.0)
    day_value = fields.Float(string = "Day value ",default=0.0)
    hour_cost = fields.Float(string = "Hour Cost",default=0.0)
    additional_constant = fields.Float(string = "Rewards " , compute='_compute_net')
    over_hours = fields.Float(string = "overtime hour",compute='_compute_net' )
    over_days = fields.Float(string = "overtime days",compute='_compute_net' )
    over_value = fields.Float(string = "overtime vlue", compute='_compute_net')
    accrual_total  = fields.Float(string = "Accrual total  ", compute='_compute_net')
    total_for_bank = fields.Float(string="Total ")
    insurance_discount = fields.Float(string = "Insurance Discount", compute='_compute_net')
    training_discount = fields.Float(string = "Training Discount", compute='_compute_net')
    traffic_fine_deduction = fields.Float(string = "Traffic Fine", compute='_compute_net')
    aramco_lost = fields.Float(string = "Aramco ", compute='_compute_net')
    advance_discount = fields.Float(string = "Advance Discount ", compute='_compute_net')
    penalty_deduction = fields.Float(string = "Penalty deduction ", compute='_compute_net')
    total_deduction = fields.Float(string="Total deduction")

    def prepare_excel_data(self):
        data = {
            'emp_id': self.emp_id,
            'emp_name': self.emp_name,
            'house_wage': self.house_wage,
            'allowances': self.allowances,
            'deductions': self.deductions,
            'mobile_allowance': self.mobile_allowance,
            'transportation_allowance': self.transportation_allowance,
            'food_allowance': self.food_allowance,
            'nature_of_work': self.nature_of_work,
            'other_allowances': self.other_allowances,
            'worked_days': self.worked_days,
            'basic_sal': self.basic_sal,
            # Add more fields as needed
        }
        return data


    def action_print_payslip_excel(self):
        print("here ")
        data = self.prepare_excel_data()

        repor_action=self.env.ref("ALTANMYA_Excel_For_Hr.report_payroll_details_xls3")
        return repor_action.report_action(docids=self.ids,data=data)



    @api.depends('name')
    def _compute_days(self):
        print("i am here ")
        _LOGGER.info("basiccccccccccccc haerererereerrererererer :")
        sum_days = 0.0
        for rec in self:
            for line in rec.worked_days_line_ids:
                if line.work_entry_type_id.code == 'ATTEND' or line.work_entry_type_id.code == 'WORK100' :
                    print("hello")
                    sum_days+=line.number_of_days
                    print("sum isss----- -", sum_days)
            rec.worked_days= sum_days
            print("work day ",sum_days, rec.worked_days )

    @api.depends('line_ids')
    def _compute_net(self):
        _LOGGER.info("basiccccccccccccc haerererereerrererererer :")
        category_mapping = {
            'Allowance': 'allowances',
            'Deduction': 'deductions',
            'House': 'house_wage',
            'Transportation': 'transportation_allowance',
            'Mobile': 'mobile_allowance',
            'Food': 'food_allowance',
            'Nature': 'nature_of_work',
            'Other': 'other_allowances',
            'Rewards':'rewards',
            'Retrived': 'retrived',
            'Totalallowances': 'total_allowances',
            'BusinessTrip': 'busniess_trip',
            'FixedOvertime': 'additional_constant',
            'OVT1':'over_value',
            'OVTD':'over_days',
            'OVTH':'over_hours',
            'Gosi': 'insurance_discount',
            'Training': 'training_discount',
            'TrafficFine': 'traffic_fine_deduction',
            'AramcoLost': 'aramco_lost',
            'Advance': 'advance_discount',
            'Penalty': 'penalty_deduction',
        }
        _LOGGER.info("\ddddddddddddddddddddddddddddddd haerererereerrererererer :")
        category_sums = {field: 0.0 for field in category_mapping.values()}
        for payslip in self:
            for line in payslip.line_ids:
                category_name = line.category_id.name
                if category_name in category_mapping:
                    field_name = category_mapping[category_name]
                    category_sums[field_name] += line.total

            for worked_days_line in payslip.worked_days_line_ids:
                workdays_name = worked_days_line.work_entry_type_id.code
                # print("work days is ", worked_days_line , workdays_name)
                # # Perform custom calculations for the specific categories
                if workdays_name == 'OVT1':
                    print("2")
                    category_sums['over_days'] += worked_days_line.number_of_days
                    category_sums['over_hours'] += worked_days_line.number_of_hours
                # elif workdays_name == 'OVTH':
                #     print("3")

                # if workdays_name == 'Attendance':
                #     print("4")
                #     category_sums['attendance'] += worked_days_line.number_of_days

            for field, value in category_sums.items():
                # print("categories is ", category_sums)
                setattr(payslip, field, value)

            if payslip.basic_sal :

                payslip.basic_sal = payslip.basic_wage
                payslip.day_value = payslip.basic_sal / 30
                payslip.hour_cost =( payslip.basic_sal / 30 ) /8
            else:
                payslip.basic_sal = 0.0






