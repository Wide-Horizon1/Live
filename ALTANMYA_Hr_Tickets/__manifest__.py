# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'ALTANMYA HR Tickets',
    'version': '1.0',
    'sequence': -200,
    'category': 'ALTANMYA HR Tickets',
    'depends': ['hr', 'approvals', 'hr_payroll', 'hr_contract', 'monthly_settlements_module', 'hr_holidays', 'ALTANMYA_Timeoff_to_Approvals'],
    'data': [
        'security/ir.model.access.csv',
        'data/ticket_approval_type.xml',
        'data/ticket_allowance_input_type.xml',
        'data/schedule_action_contract_date.xml',
        'data/ticket_allowance_settings.xml',
        'view/hr_employee_inherit_view.xml',
        'view/approval_request_view.xml',
        'view/ticket_allowance_view.xml',
        'view/hr_contract_inherit.xml',
        'view/hr_leave_inherit_view_form.xml',
        'view/hr_leave_type_inherit_view.xml',
        'view/monthly_settlements_inherit_view.xml',
        'view/approval_category_inherit_view.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
