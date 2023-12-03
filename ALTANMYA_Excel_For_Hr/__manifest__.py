# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2023-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA - Syrian Invoice Module.
#    Author: ALTANMYA for Technology(<https://tech.altanmya.net>)
#
#    This program is Licensed software: you can not modify
#   #
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'ALTANMYA - Hr Payslips',
    'author': 'Odoo mates',
    'version': '1.0',
    'website': 'www.odoomates.tech',
    'summary': 'Odoo 16 Developer',
    'depends': [
        'account_accountant',
        'hr_contract_salary',
        'hr_payroll',
        'report_xlsx' ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_excel_wizard.xml',
        # 'views/emp_inherit.xml',
        'views/payslip_inherit.xml',
        'report/report.xml',

    ],
    'license': 'LGPL-3',
}
