'''
Created on Jan 9, 2019

@author: Zuhair Hammadi
'''
from odoo import models, api, _
from odoo.exceptions import ValidationError

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    @api.constrains('state','holiday_status_id')
    def _check_attachment(self):
        for record in self:
            if record.state not in ['draft', 'cancel', 'refuse'] and record.holiday_status_id.attachment_required:
                if not self.env['ir.attachment'].search([('res_model','=', self._name), ('res_id','=', record.id)], limit = 1):
                    raise ValidationError(_('You cannot send the leave request without attaching a document.'))