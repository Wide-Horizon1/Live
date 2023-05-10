# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2023-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA Attendance Reports
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
    'name': 'ALTANMYA Attendance Reports',
    'version': '1.0',
    'category': 'Human Resources/Employees',
    'author': 'ALTANMYA - TECHNOLOGY SOLUTIONS',
    'company': 'ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP',
    'website': "https://tech.altanmya.net",
    'depends': ['ALTANMYA_Attendence_Payroll_System'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/employees_daily_attendance_wizard_views.xml',
        'wizard/employee_monthly_attendance_wizard_views.xml',
        'wizard/employees_total_att_wizard_views.xml',
        'views/employees_daily_attendance_views.xml',
        'report/unified_layout.xml',
        'report/employees_daily_attendance_report.xml',
        'report/employee_monthly_attendance_report.xml',
        'report/emp_monthly_attendance_layout.xml',
        'report/employees_total_attendance_report.xml',
        'report/employees_total_attendance_report_header.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
