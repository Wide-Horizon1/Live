from odoo import api, fields, models


class TicketAllowanceSettings(models.Model):
    _name = "ticket.allowance.settings"

    name = fields.Char(string='Name', default='Ticket Allowance')
    when_claiming = fields.Selection([('end', 'By the end of the Contract'),
                                      ('beginning', 'By the beginning of the Contract')],
                                     required=True)
    ticket_allowance_line_ids = fields.One2many('ticket.allowance.settings.lines', 'ticket_allowance_id',
                                                string='Ticket Allowance Lines')


class TicketAllowanceSettingsLines(models.Model):
    _name = "ticket.allowance.settings.lines"

    nationality_id = fields.Many2one('res.country', string='Nationality')
    cost = fields.Monetary(string='Cost of one ticket')
    currency_id = fields.Many2one('res.currency', string='Currency')
    ticket_allowance_id = fields.Many2one('ticket.allowance.settings', string='Ticket Allowance')
