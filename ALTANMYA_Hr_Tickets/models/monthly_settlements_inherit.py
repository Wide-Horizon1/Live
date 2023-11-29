from odoo import api, fields, models


class HrPayslipInputTypeInherit(models.Model):
    _inherit = "monthly.settlements"

    num_of_tick = fields.Integer(string='Number of tickets', readonly=1)
    fixed = fields.Float(name="fffffffffff", compute='_calculated_amount', store=True)
    flag = fields.Boolean(name='flag', compute='flag_method')
    date_time = fields.Datetime(string='Datetime')

    @api.depends('num_of_tick')
    def _calculated_amount(self):
        for rec in self:
            value = self.env['ticket.allowance.settings.lines'].search([('nationality_id', '=',
                                                                         rec.employee_name.country_id.id)])
            if value:
                for ticket in value:
                    total = ticket.cost * rec.num_of_tick
                    print("tortal in monthly", ticket.cost, rec.num_of_tick)
                    rec.fixed_field = total
            else:
                print("no value")

    @api.depends('type')
    def flag_method(self):
        for rec in self:
            rec.flag = False
            if rec.type.name == 'Ticket Allowance':
                rec.flag = True
