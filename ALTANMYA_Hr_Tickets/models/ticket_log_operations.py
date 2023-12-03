from odoo import api, fields, models


class TicketLogOperations(models.Model):
    _inherit = "hr.employee"

    total_cost = fields.Integer(string='Balance Of Requested Tickets', compute='_get_total_cost')
    current_tickets_num = fields.Integer(string='Requested Tickets', compute='_get_total_tickets_num')
    ticket_log_line_ids = fields.One2many('ticket.log.operations.lines', 'ticket_log_id',
                                          string='Tickets Log Lines')

    # @api.depends('emp_id')
    # def _get_employee(self):
    #     for record in self:
    #         employee = record.emp_id
    #         if employee:
    #             record.name = employee.name

    def _get_total_cost(self):

        for rec in self:
            total = 0.0
            for line in rec.ticket_log_line_ids:
                total += line.cost_of_tickets
            rec.total_cost = total
            print('total now', total)

    def _get_total_tickets_num(self):

        for rec in self:
            total = 0.0
            for line in rec.ticket_log_line_ids:
                total += line.requested_tickets_num
            rec.current_tickets_num = total
            print('total tickssss', total)


class TicketLogOperationsLines(models.Model):
    _name = "ticket.log.operations.lines"

    requested_tickets_num = fields.Integer(string='Number of tickets')
    cost_of_one_ticket = fields.Float(string='helper')
    cost_of_tickets = fields.Float(string='Cost', compute='cost_times_number')
    request_date = fields.Datetime(string='Date')
    ticket_log_id = fields.Many2one('hr.employee', string='Tickets Log')
    appr_req_id = fields.Many2one('approval.request')

    def cost_times_number(self):
        for rec in self:
            total = rec.requested_tickets_num * rec.cost_of_one_ticket
            rec.cost_of_tickets = total
