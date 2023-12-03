from odoo import api, fields, models

from datetime import datetime


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    number_of_tickets = fields.Integer(string='Main contract number', compute='_import_contract_value')
    number_of_tickets_start_end = fields.Integer(string='Ticket Allowance', compute='_compute_when_claiming')
    total_cost_left = fields.Integer(string='Balance Of Tickets', compute='_calc_balance_of_current_tickets')
    number_of_tickets_date = fields.Integer(string='Start/End', default=0)
    approved = fields.Integer(string='approved', compute='request_approve')
    approved_sum = fields.Integer(string="Total Approved Tickets", compute="_compute_approved_sum")
    calc_amount = fields.Monetary(string='Calculated Amount', compute='_calc_amount')

    def _import_contract_value(self):
        for rec in self:
            ticket_value = self.env['hr.contract.history'].search([('employee_id', '=', rec.id)], order="id desc",
                                                                  limit=1)
            state = self.env['ticket.allowance.settings'].search([('when_claiming', 'in', ['beginning', 'end'])])
            current_date = datetime.now().date()
            rec.number_of_tickets = 0
            print("all contracts ", ticket_value.contract_ids)
            for contract in ticket_value.contract_ids:
                print("contract __________ >> ", contract, state)
                print("date __________ >> ", current_date, contract.date_end)
                if contract.date_end and current_date > contract.date_end:
                    if state.when_claiming == 'end':
                        if contract.state in ['open', 'close']:
                            total = contract.contract_tickets
                            rec.number_of_tickets += total
                            print('lolo', rec.number_of_tickets)
                else:
                    if state.when_claiming != 'end':
                        if contract.state in ['open', 'close']:
                            if current_date > contract.date_start:
                                total = contract.contract_tickets
                                rec.number_of_tickets += total
                                print('start', rec.number_of_tickets)

    def _compute_when_claiming(self):
        for rec in self:
            ticket_value = self.env['hr.contract.history'].search([('employee_id', '=', rec.id)], order="id desc",
                                                                  limit=1)
            rec.number_of_tickets_start_end = 0
            for contract in ticket_value.contract_ids:
                if rec.id:
                    if contract.state in ['open', 'close']:
                        total = (rec.number_of_tickets + rec.number_of_tickets_date) - rec.approved
                        rec.number_of_tickets_start_end = total
                        print('total ', total)
                        print('num of tickets', self.number_of_tickets)
                        print('contract', self.number_of_tickets_date)
                        print('approved ', self.approved)

    @api.model
    def compute_when_start_end(self):
        state = self.env['ticket.allowance.settings'].search([('when_claiming', 'in', ['beginning', 'end'])])

        if state.when_claiming == 'beginning':
            current_date = datetime.now().date()
            employees = self.env['hr.employee'].search([])
            for employee in employees:
                total = 0
                contracts_date = self.env['hr.contract'].search([
                    ('date_start', '>=', current_date),
                    ('employee_id', '=',employee.id ),
                ])
                if contracts_date:
                    for contract in contracts_date:
                        print("employee contract", contracts_date, employee.name)
                        print("contract --------------", contract, contract.state)
                        if contract.state in ['open', 'close']:
                            print("ffffffffffffffffff", contract.contract_tickets)
                            total += contract.contract_tickets
                            employee.write({'number_of_tickets_date': total})
                            print("totaaaaaaaal", total)
                else:
                    print("zerooooooooooooooooooo")
                    employee.write({'number_of_tickets_date': 0})
        elif state.when_claiming == 'end':
            current_date = datetime.now().date()
            employees = self.env['hr.employee'].search([])
            for employee in employees:
                total = 0
                contracts_date = self.env['hr.contract'].search([
                    ('date_end', '>=', current_date),
                    ('employee_id', '=',employee.id ),
                ])
                if contracts_date:
                    for contract in contracts_date:
                        print("employee contract", contracts_date, employee.name)
                        print("contract --------------", contract, contract.state)
                        if contract.state in ['open', 'close']:

                            print("dddddddd", contract.contract_tickets)
                            total += contract.contract_tickets
                            employee.write({'number_of_tickets_date': total})
                            print("totaaaaaaaal in end ", total)
                else:
                    print("zzzzzzzzzzzzzzzzz")
                    employee.write({'number_of_tickets_date': 0})

    def request_approve(self):
        for rec in self:
            approved_value = self.env['approval.request'].search(
                [('request_status', '=', 'approved'), ('category_id.allowance_tickets', '=', True), ('state_of_req_approval', '=', 'approved'),
                 ('employee_id', '=', self.id)],
                order="id desc")
            rec.approved = 0
            for appr in approved_value:
                if appr.request_status == 'approved':
                    total = appr.number_of_tickets_
                    rec.approved += total

    def _compute_approved_sum(self):
        for employee in self:
            approved_sum = sum(employee.mapped('approved'))
            employee.approved_sum = approved_sum

    def _calc_amount(self):
        for rec in self:
            matched_ticket = self.env['ticket.allowance.settings.lines'].search(
                [('nationality_id', '=', rec.country_id.id)])
            total = 0
            for ticket in matched_ticket:
                total = ticket.cost * rec.approved_sum
            rec.calc_amount = total

    def _calc_balance_of_current_tickets(self):
        for rec in self:
            matched_ticket = self.env['ticket.allowance.settings.lines'].search(
                [('nationality_id', '=', rec.country_id.id)])
            total = 0
            for ticket in matched_ticket:
                total = ticket.cost * self.number_of_tickets_start_end
            rec.total_cost_left = total
