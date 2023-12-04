from odoo import api, fields, models


class HrLeaveTypeInherit(models.Model):
    _inherit = "hr.leave.type"

    leave_validation_type = fields.Selection(selection_add=[
        ('new', 'Link to Approvals')
    ])
    approval_id = fields.Many2one('approval.category', string="Approval Type")
