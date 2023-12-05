from odoo import api, fields, models
import logging





_LOGGER = logging.getLogger(__name__)


class Createexcelwizard(models.TransientModel):
    _name = "create.excel.wizard.payroll"  # name of Table
    _description = "Create Excel Wizard"

    def prepare_excel_data(self):

        payslip_ids = self.env['hr.payslip'].browse(self._context.get('active_ids', list()))
        _LOGGER.info("Wixaaaaaaaaaaaaaaaaaaaard :")
        data_list = []
        if payslip_ids:
            print("paslips ids is ", payslip_ids)
            for rec in payslip_ids:
                forpayslips = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                print("emplyeeeeeid <<<<<<<<<<<<<<<<",forpayslips)

                data1 = {
                    'employee_id':forpayslips.id,
                    'emp_name': rec.employee_id.name,
                    'emp_id': rec.employee_id.registration_number,
                    'house_wage': rec.house_wage,
                    'allowances': rec.allowances,
                    'deductions': rec.deductions,
                    'mobile_allowance': rec.mobile_allowance,
                    'transportation_allowance': rec.transportation_allowance,
                    'food_allowance': rec.food_allowance,
                    'nature_of_work': rec.nature_of_work,
                    'total_allowances': (rec.basic_sal) + (rec.house_wage) + (rec.food_allowance) + (
                        rec.transportation_allowance) + (rec.mobile_allowance) + (rec.nature_of_work),
                    'other_allowances': rec.other_allowances,
                    'worked_days': rec.worked_days,
                    'basic_sal': rec.basic_sal,
                    'rewards': rec.rewards,
                    'retrived': rec.retrived,
                    'busniess_trip': rec.busniess_trip,
                    'day_value': rec.day_value,
                    'hour_cost': rec.hour_cost,
                    'additional_constant': rec.additional_constant,
                    'over_hours': rec.over_hours,
                    'over_days': rec.over_days,
                    'over_value': rec.over_value,
                    'accrual_total': (rec.other_allowances) + (rec.busniess_trip) + (rec.rewards) + (rec.over_value) + (rec.retrived) + (rec.additional_constant),
                    'total_for_bank':(rec.transportation_allowance) + (rec.mobile_allowance) + (rec.food_allowance) + (rec.nature_of_work) + (rec.other_allowances) + (rec.busniess_trip) + (rec.rewards) + (rec.retrived) + (rec.additional_constant) + (rec.over_value),
                    'insurance_discount': rec.insurance_discount,
                    'training_discount': rec.training_discount,
                    'traffic_fine_deduction': rec.traffic_fine_deduction,
                    'aramco_lost': rec.aramco_lost,
                    'advance_discount': rec.advance_discount,
                    'penalty_deduction': rec.penalty_deduction,
                    'total_deduction': (rec.insurance_discount) + (rec.training_discount) + (rec.traffic_fine_deduction) + (rec.advance_discount) + (rec.penalty_deduction) + (rec.aramco_lost),
                    'net_sal':rec.net_wage,
                    # Add more fields as needed
                }
                data_list.append(data1)
            print("data is ", data_list)
            _LOGGER.info('data list :', data_list)
            _LOGGER.info('data list 222222222222222 :',data1)
            data = {
                'records': data_list,

            }
            print("data", data)
        repor_action = self.env.ref("ALTANMYA_Excel_For_Hr.report_payroll_details_xls3")
        return repor_action.report_action(self, data=data)

