# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Altanmya-Exceptional Reports',
    'version': '1.0',
    'sequence': -200,
    'category': 'Altanmya-Exceptional Reports',
    'depends': ['account'],
    'data': [
        'views/account_form_view.xml',
        'report/report_info.xml',
        'report/invoice_exceptional_report.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
