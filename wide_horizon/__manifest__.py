# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Wide Horizon',
    'version': '1.0',
    'sequence': -201,
    'depends': ['base', 'hr', 'hr_contract', 'hr_payroll'],
    'data': [
        'data/cron.xml',
        'views/hr_contract.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}