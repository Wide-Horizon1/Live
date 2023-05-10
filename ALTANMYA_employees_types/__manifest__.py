# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2022-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA Attendance Device Adaptor.
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
    'name': 'ALTANMYA employee types',
    'version': '1.0',
    'summary': '',
    'sequence': 10,
    'description': "ALTANMYA employee types management software",
    'category': 'Human Resources/Employees',
    'author': 'ALTANMYA - TECHNOLOGY SOLUTIONS',
    'company': 'ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP',
    'website': "https://tech.altanmya.net",
    'depends': [
        'hr_contract', 'hr',
        'fleet',
    ],
    'data': [
        'security/security.xml',
        'views/hr_employee_views_inherit.xml',
        'views/hr_views_inherit.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
