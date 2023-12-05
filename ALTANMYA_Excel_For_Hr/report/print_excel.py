from odoo import models
import base64
import io
import logging

_LOGGER = logging.getLogger(__name__)


class ExcelPayrollXlsx(models.AbstractModel):
    _name = 'report.payslips.details.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, emp):
        print("generated")

        fields_to_include = [
            'emp_id', 'emp_name', 'worked_days', 'basic_sal', 'house_wage', 'transportation_allowance',
            'food_allowance', 'mobile_allowance', 'nature_of_work', 'total_allowances',
            'other_allowances', 'busniess_trip', 'rewards', 'retrived', 'day_value', 'hour_cost', 'additional_constant',
            'over_hours', 'over_days', 'over_value', 'accrual_total', 'total_for_bank', 'insurance_discount',
            'training_discount', 'traffic_fine_deduction', 'aramco_lost', 'advance_discount', 'penalty_deduction',
            'total_deduction', 'net_sal'
        ]
        fields_to_capitalize = ['الرقم الوظيفي', 'الأسم', 'عدد أيام العمل', 'الراتب الأساسي', 'بدل السكن',
                                'بدل مواصلات ',
                                'بدل طعام', 'بدل جوال', 'بدل طبيعة عمل', 'إجمالي الراتب', 'مستحقات اخرى', 'رحلة عمل',
                                'مكافأة', 'ردود',
                                'قيمة اليوم', 'قيمة الساعة', 'اضافي ثابت', 'ساعات الإضافي', 'ايام الإضافي',
                                'قيمة الإضافي', 'إجمالي الإستحقاق', 'اجمالي البدلات+الاضافي للملف البنكي',
                                'خصم التأمينات', 'خصم التدريب',
                                'خصم مخالفة مرورية', 'فاقد ارامكو', 'خصم سلفة', 'خصم جزاء', 'إجمالي الخصم',
                                'صافي الراتب']

        sheet = workbook.add_worksheet('Excel ')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format(
            {'bold': True, 'bg_color': '#038d71', 'font_color': 'black', 'border': 1})
        border_format = workbook.add_format({'border': 1})
        header_height = 30  # Adjust the height value as needed
        sheet.set_row(0, header_height)  # Adjust the height value as needed
        format1 = workbook.add_format({'bold': True, 'bg_color': '#BFBFBF', 'font_color': 'black', 'border': 1})
        format2 = workbook.add_format({'bold': True, 'bg_color': '#CFE2F3', 'font_color': 'black', 'border': 1})
        format3 = workbook.add_format({'bold': True, 'bg_color': '#F9CB9C', 'font_color': 'black', 'border': 1})
        format4 = workbook.add_format({'bold': True, 'bg_color': 'black', 'font_color': 'white', 'border': 1})
        format5 = workbook.add_format({'bold': True, 'bg_color': 'blue', 'font_color': 'black', 'border': 1})

        for col, field_name in enumerate(fields_to_capitalize):
            if col < 2:  # Apply format1 to the first 3 columns
                sheet.write(0, col, field_name.capitalize(), format1)
            elif 2 <= col <= 6:
                sheet.write(0, col, field_name.capitalize(), format2)
            elif 7 <= col <= 12:
                sheet.write(0, col, field_name.capitalize(), format3)
            elif 13 <= col <= 19:
                sheet.write(0, col, field_name.capitalize(), format2)
            elif 19 <= col <= 20:
                sheet.write(0, col, field_name.capitalize(), format4)
            elif 20 <= col <= 21:
                sheet.write(0, col, field_name.capitalize(), format5)
            elif 21 <= col <= 27:
                sheet.write(0, col, field_name.capitalize(), format3)
            elif 28 <= col <= 30:
                sheet.write(0, col, field_name.capitalize(), format4)

        for col, field_name in enumerate(fields_to_capitalize):
            sheet.set_column(col, col, len(field_name) + 2)

        row = 1
        employee_data = {}
        for employee_id in data['records']:
            print("employee_id",employee_id.get('employee_id'))
            emp = self.env['hr.employee'].sudo().browse(employee_id.get('employee_id'))
            print("emp iddddd iss---------------- ",emp.id)
            emp_id = employee_id.get('employee_id')
            print("dataaaa get ",emp_id)
            # Check if the employee is already in the dictionary
            if emp_id in employee_data:
                employee = employee_data[emp_id]
            else:
                employee = {field: 0.0 for field in fields_to_include}
                employee['employee_id'] = emp_id
                employee['emp_id'] = employee_id.get('emp_id')
                employee['emp_name'] = employee_id.get('emp_name')
                    # Initialize a new employee entry

            # Aggregate the data for the employee
            employee['worked_days'] += employee_id.get('worked_days', 0.0)
            employee['basic_sal'] += employee_id.get('basic_sal', 0.0)
            employee['house_wage'] += employee_id.get('house_wage', 0.0)
            employee['transportation_allowance'] += employee_id.get('transportation_allowance', 0.0)
            employee['food_allowance'] += employee_id.get('food_allowance', 0.0)
            employee['mobile_allowance'] += employee_id.get('mobile_allowance', 0.0)
            employee['nature_of_work'] += employee_id.get('nature_of_work', 0.0)
            employee['total_allowances'] += employee_id.get('total_allowances', 0.0)
            employee['other_allowances'] += employee_id.get('other_allowances', 0.0)
            employee['busniess_trip'] += employee_id.get('busniess_trip', 0.0)
            employee['rewards'] += employee_id.get('rewards', 0.0)
            employee['retrived'] += employee_id.get('retrived', 0.0)
            employee['day_value'] += employee_id.get('day_value', 0.0)
            employee['hour_cost'] += employee_id.get('hour_cost', 0.0)
            employee['additional_constant'] += employee_id.get('additional_constant', 0.0)
            employee['over_hours'] += employee_id.get('over_hours', 0.0)
            employee['over_days'] += employee_id.get('over_days', 0.0)
            employee['over_value'] += employee_id.get('over_value', 0.0)
            employee['accrual_total'] += employee_id.get('accrual_total', 0.0)
            employee['total_for_bank'] += employee_id.get('total_for_bank', 0.0)
            employee['insurance_discount'] += employee_id.get('insurance_discount', 0.0)
            employee['training_discount'] += employee_id.get('training_discount', 0.0)
            employee['traffic_fine_deduction'] += employee_id.get('traffic_fine_deduction', 0.0)
            employee['aramco_lost'] += employee_id.get('aramco_lost', 0.0)
            employee['advance_discount'] += employee_id.get('advance_discount', 0.0)
            employee['penalty_deduction'] += employee_id.get('penalty_deduction', 0.0)
            employee['total_deduction'] += employee_id.get('total_deduction', 0.0)
            employee['net_sal'] += employee_id.get('net_sal', 0.0)

            # Add more fields as needed

            # Update the employee's data in the dictionary
            employee_data[emp_id] = employee
        row = 1
        print("emplyee data ",employee_data)
        for employee , emp_data in employee_data.items():
            print("employeee dataaa values------",employee)
            print("employeee dataaa data------",emp_data)
            col = 0
            row_data = [
                emp_data['emp_id'],
                emp_data['emp_name'],
                emp_data['worked_days'],
                emp_data['basic_sal'],
                emp_data['house_wage'],
                emp_data['transportation_allowance'],
                emp_data['food_allowance'],
                emp_data['mobile_allowance'],
                emp_data['nature_of_work'],
                emp_data['total_allowances'],
                emp_data['other_allowances'],
                emp_data['busniess_trip'],
                emp_data['rewards'],
                emp_data['retrived'],
                emp_data['day_value'],
                emp_data['hour_cost'],
                emp_data['additional_constant'],
                emp_data['over_hours'],
                emp_data['over_days'],
                emp_data['over_value'],
                emp_data['accrual_total'],
                emp_data['total_for_bank'],
                emp_data['insurance_discount'],
                emp_data['training_discount'],
                emp_data['traffic_fine_deduction'],
                emp_data['aramco_lost'],
                emp_data['advance_discount'],
                emp_data['penalty_deduction'],
                emp_data['total_deduction'],
                emp_data['net_sal'],


            ]
            sheet.write_row(row, col, row_data)
            row += 1
        print("amjad b6eee5")
