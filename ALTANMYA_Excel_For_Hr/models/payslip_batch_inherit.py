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
    house_wage=fields.Float(compute='_compute_fields')
    allowances=fields.Float(compute='_compute_fields')
    deductions =fields.Float(compute='_compute_fields')
    mobile_allowance =fields.Float(compute='_compute_fields',default=0.0)
    transportation_allowance =fields.Float(compute='_compute_fields',default=0.0)
    food_allowance =fields.Float(compute='_compute_fields',default=0.0)
    nature_of_work=fields.Float(compute='_compute_fields',default=0.0)
    total_allowances=fields.Float(compute='_compute_fields',default=0.0)
    other_allowances =fields.Float(compute='_compute_fields',default=0.0)
    busniess_trip =fields.Float(compute='_compute_fields',default=0.0)
    worked_days= fields.Float(string = "worked days" , compute='_compute_days',default=0.0)
    basic_sal = fields.Float(string = "Baseic days" ,compute='_compute_fields')
    rewards = fields.Float(string = "Rewards " , compute='_compute_fields',default=0.0)
    retrived = fields.Float(string = "Retrived " , compute='_compute_fields',default=0.0)
    day_value = fields.Float(string = "Day value ",default=0.0)
    hour_cost = fields.Float(string = "Hour Cost",default=0.0)
    additional_constant = fields.Float(string = "Rewards " , compute='_compute_fields')
    over_hours = fields.Float(string = "overtime hour",compute='_compute_fields' )
    over_days = fields.Float(string = "overtime days",compute='_compute_fields' )
    over_value = fields.Float(string = "overtime vlue", compute='_compute_fields')
    accrual_total  = fields.Float(string = "Accrual total  ", compute='_compute_fields')
    total_for_bank = fields.Float(string="Total ")
    insurance_discount = fields.Float(string = "Insurance Discount", compute='_compute_fields')
    training_discount = fields.Float(string = "Training Discount", compute='_compute_fields')
    traffic_fine_deduction = fields.Float(string = "Traffic Fine", compute='_compute_fields')
    aramco_lost = fields.Float(string = "Aramco ", compute='_compute_fields')
    advance_discount = fields.Float(string = "Advance Discount ", compute='_compute_fields')
    penalty_deduction = fields.Float(string = "Penalty deduction ", compute='_compute_fields')
    total_deduction = fields.Float(string="Total deduction")

    @api.depends('name')
    def _compute_fields(self):
        category_mapping = {
            'Allowance': 'allowances',
            'Deduction': 'deductions',
            'House': 'house_wage',
            'Transportation': 'transportation_allowance',
            'Mobile': 'mobile_allowance',
            'Food': 'food_allowance',
            'Nature': 'nature_of_work',
            'Other': 'other_allowances',
            'Rewards': 'rewards',
            'Retrived': 'retrived',
            'Totalallowances': 'total_allowances',
            'BusinessTrip': 'busniess_trip',
            'FixedOvertime': 'additional_constant',
            'OVT1': 'over_value',
            'OVTD': 'over_days',
            'OVTH': 'over_hours',
            'Gosi': 'insurance_discount',
            'Training': 'training_discount',
            'TrafficFine': 'traffic_fine_deduction',
            'AramcoLost': 'aramco_lost',
            'Advance': 'advance_discount',
            'Penalty': 'penalty_deduction',
        }
        for payslip in self :
            print("record" ,payslip )

            if not payslip.basic_sal :
                payslip.basic_sal = payslip.basic_wage
                payslip.day_value = payslip.basic_sal / 30
                payslip.hour_cost =( payslip.basic_sal / 30 ) /8

            else:
                payslip.basic_sal = 0.0


            category_sums = {field: 0.0 for field in category_mapping.values()}

            for line in payslip.line_ids:
                category_name = line.category_id.name
                if category_name in category_mapping:
                    field_name = category_mapping[category_name]
                    category_sums[field_name] += line.total

            for worked_days_line in payslip.worked_days_line_ids:
                workdays_name = worked_days_line.work_entry_type_id.code
                if workdays_name == 'OVT1':
                    print("2")
                    category_sums['over_days'] += worked_days_line.number_of_days
                    category_sums['over_hours'] += worked_days_line.number_of_hours


            for field, value in category_sums.items():
                setattr(payslip, field, value)

    def action_print_payslip_excel(self):
        print("here ")
        data = self.prepare_excel_data()

        repor_action=self.env.ref("ALTANMYA_Excel_For_Hr.report_payroll_details_xls3")
        return repor_action.report_action(docids=self.ids,data=data)
    @api.depends('name')
    def _compute_days(self):
        print("i am here ")
        for rec in self:
            sum_days = 0.0
            _LOGGER.info("basiccccccccccccc haerererereerrererererer compute :")
            _LOGGER.info(rec)
            _LOGGER.info(self)
            for line in rec.worked_days_line_ids:
                if line.work_entry_type_id.code == 'ATTEND' or line.work_entry_type_id.code == 'WORK100' :
                    
                    sum_days+=line.number_of_days

                    _LOGGER.info(sum_days)
            rec.worked_days= sum_days


