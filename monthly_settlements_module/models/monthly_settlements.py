from collections import defaultdict

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_round



class MonthlySettlements(models.Model):
    _name = "monthly.settlements"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Monthly Settlements Sys"

    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get('monthly.settlements'), tracking=True)

    employee_name = fields.Many2one('hr.employee', string='Employee Name', required=True, tracking=True,copy=True, domain="[('company_id', '=', company_id)]")
    type = fields.Many2one('hr.payslip.input.type', string='Type', tracking=True,copy=True,required=True)
    total_result = fields.Float(string='Total Result', compute="compute_total_result", tracking=True,copy=True)
    description = fields.Char(string='Description', tracking=True,copy=True)
    amount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage')
    ], string='Amount Type', required=True, default='fixed', tracking=True,copy=True)
    total_amount = fields.Float(string='Total Amount Percentage',
                                   compute="compute_total_amount", tracking=True)
    # percentage_of = fields.Many2one('hr.salary.rule', string='Percentage Of',
    #                                 help='Percentage calculated on Basic or Gross Salary',
    #                                 domain="[('category_id.name', 'in', ['Gross', 'Basic'])]", tracking=True
    #                                 )
    percentage_off = fields.Selection([
        ('basic', 'Basic'),
    ], string='Percentage Of',
        help='Percentage calculated on Basic or Gross Salary',
        tracking=True,default='basic',required=True,copy=True
    )

    percentage = fields.Float(string='Percentage', tracking=True,copy=True)

    num_of_month = fields.Integer(
        string='Number of Months',
        default=1, required=True, compute='action_calculate', store=True, tracking=True
    )

    current_user_to_approve = fields.Integer(string='Admin', tracking=True,copy=True)
    fixed_field = fields.Float(string='Total Amount Fixed', tracking=True )
    date = fields.Date(string='Date of Settlement', required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', tracking=True,copy=True)
    monthly_settlements_lines_ids = fields.One2many('monthly.settlements.lines', 'monthly_settlements_lines_id',
                                                    string="Monthly Settlements Lines", tracking=True)
    result = fields.Float(string='Result', tracking=True)
    result_to_type = fields.Float(string='Result', tracking=True,copy=True)

    state = fields.Selection(selection=lambda self: self.get_stages(), string='Status',
                             readonly=True, copy=False, index=True, tracking=3, default='draft')
    monthly_settlements_type = fields.Many2one('monthly.settlements.stage.type', string='M.S Type',
                                               compute='_calc_stage',
                                               # compute='test',
                                               inverse='_get_type', tracking=3,
                                               store=True)

    min_range = fields.Float(string="From", store=True, tracking=True)
    max_range = fields.Float(string="To", store=True, tracking=True)
    clicked_m_s = fields.Boolean(string="For Compute", tracking=True,copy=True)
    current_user_id = fields.Many2one('res.users', string='Current User', tracking=True,copy=True)
    show = fields.Boolean(compute="compute_show", tracking=True,copy=True)

    total_rate = fields.Float(compute='_compute_total_rate', string='Total Amount', store=True, tracking=True)

    @api.depends('monthly_settlements_lines_ids.total_amount_lines')
    def _compute_total_rate(self):
        for record in self:
            total_amount = sum(
                line.total_amount_lines for line in record.monthly_settlements_lines_ids if not line.delay)
            print("line issss ", total_amount)


            record.total_rate = total_amount
            # for line in record.monthly_settlements_lines_ids:
            #     if line.delay == False :
            #
            #         print("line issss ", line.delay)
            #
            #         total_amount = sum(line.total_amount_lines)
            #         print("total amount " , total_amount)
            #         record.total_rate = total_amount
            #         print("llllllllllllllllllll",record.total_rate)

    # @api.constrains('total_rate')
    # @api.depends('monthly_settlements_lines_ids.delay')
    def write(self,vals):
        for record in self:
            # self._compute_total_rate()
            print("linnnnnnnnnnnnnn",float_round(record.total_rate,2) ,record.fixed_field,record.monthly_settlements_lines_ids)

            result = super(MonthlySettlements, self).write(vals)
            for rec in self:
                if rec.amount_type == 'fixed':
                    for line in rec.monthly_settlements_lines_ids:
                        print("nnnnnnnnnnnnnnnnn",
                              line.delay)

                        if float_round(rec.total_rate,2) > float_round(rec.fixed_field,2) :
                            raise ValidationError("The sum of total amount line not in range ")
                        elif float_round(rec.total_rate,2) < float_round(rec.fixed_field,2) :
                            raise ValidationError("The sum of total amount line not in range ")
                elif rec.amount_type == 'percentage':
                    for line in rec.monthly_settlements_lines_ids:
                        print("nnnnnnnnnnnnnnnnn",
                              line.delay)

                        if float_round(rec.total_rate, 2) > float_round(rec.total_amount, 2):
                            raise ValidationError("The sum of total amount line not in range ")
                        elif float_round(rec.total_rate, 2) < float_round(rec.total_amount, 2):
                            raise ValidationError("The sum of total amount line not  range ")

            return result

    @api.depends('num_of_month', 'result', 'total_result','fixed_field')
    def action_calculate(self):
        for rec in self:
            print("hhello 2")
            for record in self:
                if record.amount_type == 'fixed':
                    if record.fixed_field and record.num_of_month and record.date:
                        if record.monthly_settlements_lines_ids:
                            record.monthly_settlements_lines_ids.unlink()
                        cu_date = record.date
                        for rec in range(record.num_of_month):
                            res = record.fixed_field / record.num_of_month
                            line_vals = {
                                'date_lines': cu_date,
                                'total_amount_lines': res,
                                'description_lines': record.description,
                                'delay': False,
                            }
                            record.create_record(line_vals)
                            cu_date = fields.Date.to_string(fields.Date.from_string(cu_date) + relativedelta(months=1))
                    else:
                        record.monthly_settlements_lines_ids = False
                elif record.amount_type == 'percentage':
                    print("percentage")
                    if record.total_amount and record.num_of_month and record.date:
                        if record.monthly_settlements_lines_ids:
                            record.monthly_settlements_lines_ids.unlink()
                        cu_date = record.date
                        for rec in range(record.num_of_month):
                            res = record.total_amount / record.num_of_month
                            line_vals = {
                                'date_lines': cu_date,
                                'total_amount_lines': res,
                                'description_lines': record.description,
                                'delay': False,
                            }
                            record.create_record(line_vals)
                            cu_date = fields.Date.to_string(fields.Date.from_string(cu_date) + relativedelta(months=1))
                    else:
                        record.monthly_settlements_lines_ids = False

            #
            #
            # if rec.date:
            #     vals = {
            #         'employee_name': rec.employee_name.id,
            #         'type': rec.type.id,
            #         'description': rec.description,
            #         'amount_type': rec.amount_type,
            #         # 'percentage_of': rec.percentage_of,
            #         'percentage': rec.percentage,
            #         'num_of_month': rec.num_of_month,
            #         'current_user_to_approve': rec.current_user_to_approve,
            #         # 'fixed_field': rec.fixed_field,
            #         'date': rec.date,
            #         'min_range': rec.min_range,
            #         'max_range': rec.max_range,
            #         'current_user_id': rec.current_user_id.id,
            #         'result': rec.result,
            #         'total_result': rec.total_result,
            #     }
            #     if not rec.monthly_settlements_lines_ids:
            #
            #         print("or heree ======================")
            #         if rec.amount_type == 'percentage':
            #             if rec.num_of_month:
            #                 result = rec.total_amount / rec.num_of_month
            #             else:
            #                 result = 0
            #         elif rec.amount_type == 'fixed':
            #             result = rec.total_result / rec.num_of_month if rec.num_of_month else 0
            #             print("result is ", result)
            #         rec.result = result
            #         # rec.fixed_field = result
            #         rec.create_record(vals)
            #         for line in rec.monthly_settlements_lines_ids:
            #             line.total_amount_lines = rec.result
            #     else:
            #         print("i am here -------------")
            #         if rec.amount_type == 'percentage':
            #             if rec.num_of_month:
            #                 result = rec.total_amount / rec.num_of_month
            #             else:
            #                 result = 0
            #         elif rec.amount_type == 'fixed':
            #             result = rec.total_result / rec.num_of_month if rec.num_of_month else 0
            #             print("result is(2) ", result)
            #         rec.result = result
            #         # rec.fixed_field = result
            #         rec.create_record(vals)
            #         for line in rec.monthly_settlements_lines_ids:
            #             line.total_amount_lines = rec.result
            #
            #         for line in rec.monthly_settlements_lines_ids:
            #             if rec.date:
            #                 if rec.num_of_month:
            #                     entry_num_of_month = rec.num_of_month
            #                     old_value = rec.result
            #                     if len(rec.monthly_settlements_lines_ids) > rec.num_of_month:
            #                         print(" i dont care---------------------------- ")
            #                         rec.num_of_month = entry_num_of_month
            #                     elif len(rec.monthly_settlements_lines_ids) < rec.num_of_month:
            #                         print(" i love it ---------------------------- ")
            #                         rec.num_of_month = entry_num_of_month
            # res = rec.unlink_line_if_found(vals)

    # @api.onchange('monthly_settlements_lines_ids')
    # def _onchange_lines(self):
    #     for record in self:
    #         change_messages = []
    #
    #         for line in record.monthly_settlements_lines_ids:
    #             if line.is_changed:
    #                 change_messages.append(f"Changed '{line.delay}'")
    #
    #         if change_messages:
    #             print("kkkkkkkkkkkkkkkkkkkkkk")
    #             message = '{} made the following changes:\n{}'.format(record.employee_name, '\n'.join(change_messages))
    #             rec = record.monthly_settlements_lines_ids.message_post(body=message, subject='Changes')



    # @api.onchange('monthly_settlements_lines_ids')
    # def _onchange_lines(self):
    #     for record in self:
    #         message = '{} printed {} file'.format(record.employee_name)
    #         rec = record.monthly_settlements_lines_ids.message_post(body=message, subject='Printing')
    #         # rec.update({'date': datetime.now()})

    @api.constrains('num_of_month')
    def _check_num_of_month(self):
        for record in self:
            if record.num_of_month <= 0:
                raise ValidationError(_("Number of months must be grater than zero !! ."))



    def _process_calculation(self, rec, tot):
        stage_domain = self.env["monthly.settlements.stage.type"].search([])
        for stage_domain_type in stage_domain:
            mi = stage_domain_type.min_range
            ma = stage_domain_type.max_range
            ret_type = self.env['monthly.settlements.stage.type'].search([
                ('min_range', '<=', tot),
                ('max_range', '>=', tot)], limit=1)
            if ret_type:
                rec.min_range = ret_type.min_range
                rec.max_range = ret_type.max_range

            print("ret type ", ret_type)
            if not ret_type:
                ret_type = self.env['monthly.settlements.stage.type'].search(
                    [('currency', '=', False), ('min_range', '<=', tot),
                     ('max_range', '>=', tot)], limit=1)
                print(" ret type in false ", ret_type)
            self.monthly_settlements_type = ret_type
            print("monthly type ++++", self.monthly_settlements_type)

    def process_payslips(self, employee_id, state, date_from, date_to):
        salary_slips_to_pay = self.env['hr.payslip'].search([
            ('employee_id', "=", employee_id),
            ('state', '=', state),
            # ('date_from', '<=', date_from),
            # ('date_to', '>=', date_to)
        ])
        print("all we have in to pay", salary_slips_to_pay)
        for payslip in salary_slips_to_pay:
            mo = self.env['monthly.settlements'].search([("employee_name", "=", employee_id),
                                                         ('monthly_settlements_lines_ids.date_lines', '>=',
                                                          payslip.date_from),
                                                         ('monthly_settlements_lines_ids.date_lines', '<=',
                                                          payslip.date_to),
                                                         ('state', '=',
                                                          'done'),
                                                         ])
            for mo_record in mo:
                print("monthly is :", mo_record)
                for contract in payslip.contract_id:
                    # print("contract number is: ", payslip.contract_id)
                    for lines in mo_record.monthly_settlements_lines_ids:
                        print("lines date is ", lines.date_lines, payslip.date_from, payslip.date_to,type(contract.date_start),type(lines.date_lines))
                        if isinstance(contract.date_start, date) and isinstance(contract.date_end, date) and isinstance(
                                lines.date_lines, date):


                            if contract.state == 'open' and (lines.date_lines >= payslip.date_from and lines.date_lines <= payslip.date_to) and  (contract.date_start <= lines.date_lines <= contract.date_end) and lines.delay == False:
                                print("here")
                                lines.status = 'done'
                                inputs = payslip.env['hr.payslip.input'].search([
                                    ('payslip_id', '=', payslip.id),
                                    ('input_type_id', '=', mo_record.type.id),
                                    ('name', '=', lines.description_lines),
                                    ('amount', '=', lines.total_amount_lines),
                                ])
                                if not inputs:
                                    x = {
                                        'payslip_id': payslip.id,
                                        'input_type_id': mo_record.type.id,
                                        'name': lines.description_lines,
                                        'amount': lines.total_amount_lines,
                                    }
                                    payslip.env['hr.payslip.input'].create(x)

                        else:
                            raise ValidationError("Date Of Contract doesn't set  !!!")

    """
        def test : 
        Use this method to check if res is within the domain or not    
    """

    @api.onchange('description')
    def _onchange_description(self):
        # Loop through all the lines associated with this record
        for line in self.monthly_settlements_lines_ids:
            line.description_lines = self.description




    def unlink_line_if_found(self, vals):
        for rec in self:
            for line in rec.monthly_settlements_lines_ids:
                line.unlink()
            # rec.create_record(vals)

    # @api.depends('num_of_month', 'result', 'total_result')
    # def action_calculate(self):
    #     for rec in self:
    #         print("hhello 2")
    #         if rec.date:
    #             vals = {
    #                 'employee_name': rec.employee_name.id,
    #                 'type': rec.type.id,
    #                 'description': rec.description,
    #                 'amount_type': rec.amount_type,
    #                 # 'percentage_of': rec.percentage_of,
    #                 'percentage': rec.percentage,
    #                 'num_of_month': rec.num_of_month,
    #                 'current_user_to_approve': rec.current_user_to_approve,
    #                 # 'fixed_field': rec.fixed_field,
    #                 'date': rec.date,
    #                 'min_range': rec.min_range,
    #                 'max_range': rec.max_range,
    #                 'current_user_id': rec.current_user_id.id,
    #                 'result': rec.result,
    #                 'total_result': rec.total_result,
    #             }
    #             if not rec.monthly_settlements_lines_ids:
    #
    #                 print("or heree ======================")
    #                 if rec.amount_type == 'percentage':
    #                     if rec.num_of_month:
    #                         result = rec.total_amount / rec.num_of_month
    #                     else:
    #                         result = 0
    #                 elif rec.amount_type == 'fixed':
    #                     result = rec.total_result / rec.num_of_month if rec.num_of_month else 0
    #                     print("result is ", result)
    #                 rec.result = result
    #                 # rec.fixed_field = result
    #                 rec.create_record(vals)
    #                 for line in rec.monthly_settlements_lines_ids:
    #                     line.total_amount_lines = rec.result
    #             else:
    #                 print("i am here -------------")
    #                 if rec.amount_type == 'percentage':
    #                     if rec.num_of_month:
    #                         result = rec.total_amount / rec.num_of_month
    #                     else:
    #                         result = 0
    #                 elif rec.amount_type == 'fixed':
    #                     result = rec.total_result / rec.num_of_month if rec.num_of_month else 0
    #                     print("result is(2) ", result)
    #                 rec.result = result
    #                 # rec.fixed_field = result
    #                 rec.create_record(vals)
    #                 for line in rec.monthly_settlements_lines_ids:
    #                     line.total_amount_lines = rec.result
    #
    #                 for line in rec.monthly_settlements_lines_ids:
    #                     if rec.date:
    #                         if rec.num_of_month:
    #                             entry_num_of_month = rec.num_of_month
    #                             old_value = rec.result
    #                             if len(rec.monthly_settlements_lines_ids) > rec.num_of_month:
    #                                 print(" i dont care---------------------------- ")
    #                                 rec.num_of_month = entry_num_of_month
    #                             elif len(rec.monthly_settlements_lines_ids) < rec.num_of_month:
    #                                 print(" i love it ---------------------------- ")
    #                                 rec.num_of_month = entry_num_of_month
    #                 # res = rec.unlink_line_if_found(vals)
    def create_record(self, vals):
        for record in self:
            if 'date_lines' in vals:
                self.env['monthly.settlements.lines'].create({
                    'date_lines': vals['date_lines'],
                    'description_lines': vals.get('description_lines', record.description),
                    'total_amount_lines': vals.get('total_amount_lines', record.fixed_field / record.num_of_month),
                    'monthly_settlements_lines_id': record.id,
                })

    @api.depends('total_result', 'min_range', 'max_range', 'monthly_settlements_type')
    def test(self):
        for rec in self:
            stage_domain = self.env["monthly.settlements.stage.type"].search([])
            for stage_domain_type in stage_domain:
                res = rec.total_result
                mi = stage_domain_type.min_range
                ma = stage_domain_type.max_range
                if mi <= res <= ma:
                    rec.min_range = mi
                    rec.max_range = ma
                    rec.monthly_settlements_type = stage_domain_type.name

    @api.depends('total_result', 'min_range', 'max_range', 'monthly_settlements_type')
    def _calc_stage(self):

        tot = 0
        currid = 0

        for rec in self:
            if rec.amount_type == 'percentage':
                print(" calc stage  here percentage ")
                self._process_calculation(rec, rec.total_amount)
            else:
                print(" calc stage  here  fixed")

                self._process_calculation(rec, rec.fixed_field)

    def check_stage(self, ascending=True):
        count_approve = self.env['monthly.settlements.order.user.pending'].search_count([('state', '=', self.state)
                                                                                            , (
                                                                                             'monthly_settlements_id',
                                                                                             '=',
                                                                                             self.id)
                                                                                            ,
                                                                                         ('status', '=', 'approve')])
        current_stage = self.env['monthly.settlements.stage'].sudo().search([('code', '=', self.state)], limit=1)

        print("monthely type ", self.monthly_settlements_type)
        print("monthely type stage ", self.monthly_settlements_type.stages)
        newlist = sorted(self.monthly_settlements_type.stages, key=lambda x: x.stage_order)
        print("new list ", newlist)
        print("current stage is  ", current_stage)
        print("count approve stage is  ", count_approve)
        if len(current_stage.stage_users) == count_approve:
            print("current is ", current_stage.code)
            print("current is ", current_stage.stage_users)
            print("current is ", current_stage.stage_users)
            if current_stage.code == newlist[len(newlist) - 1].code:
                print("################")

                print("from here 1 ")
                salary_slips_to_pay = self.env['hr.payslip'].search([
                    ("employee_id", "=", self.employee_name.ids),
                    ("state", "=", "verify")
                ])
                self.clicked_m_s = True
                print("from here all we have in to pay 2", salary_slips_to_pay)
                salary_sorted = salary_slips_to_pay.sorted(key=lambda r: r.number, reverse=not ascending)
                print("from hereall we have in to pay with sorte 3 ", salary_sorted)
                record_created = False
                self.state = 'done'
                self.action_create_record(ascending=True)

                # super(MonthlySettlements, self).action_submit()
            else:
                print("$$$$$$$$$$$$$$$$$$$")
                for x in range(0, len(newlist) - 1):
                    print("xxxxxxxxxxxxxxxxxxx", x, newlist, len(newlist) - 1)
                    if newlist[x].code == current_stage.code:
                        self.state = newlist[x + 1].code
                        print("state is sssssss", self.state)
                        current_stage = self.env['monthly.settlements.stage'].sudo().search([('code', '=', self.state)],
                                                                                            limit=1)
                        uorder = 0
                        rec_id = self.env['ir.model'].sudo().search([('model', '=', 'monthly.settlements')], limit=1)
                        # print(rec_id)
                        qquery = " select seq,res_users_id from monthly_settlements_stage_res_users_rel  where monthly_settlements_stage_id=" + str(
                            current_stage.id)
                        self.env.cr.execute(qquery)
                        stage_users = self.env.cr.fetchall()
                        sorted_users = sorted(stage_users)
                        print("stage user isss9999999", stage_users)
                        for user in sorted_users:
                            print("stage line is ", user, stage_users)

                            print("user[1]", user)
                            uorder = uorder + 1
                            if uorder == 1:
                                print("1111")
                                self.env['monthly.settlements.order.user.pending'].create({
                                    'user': user[1],
                                    'monthly_settlements_id': self.id,
                                    'state': self.state,
                                    'status': 'waiting',
                                    'user_order': uorder
                                })
                                self.write({'current_user_id': user[1]})
                                self.env['mail.activity'].sudo().create({
                                    'activity_type_id': 4,
                                    'date_deadline': date.today(),
                                    'summary': 'Request to approve',
                                    'user_id': user[1],
                                    'res_model_id': rec_id.id,
                                    'res_id': self.id
                                })
                            else:
                                print("000000")
                                print("user is ", user, uorder)
                                self.env['monthly.settlements.order.user.pending'].create({
                                    'user': user[1],
                                    'monthly_settlements_id': self.id,
                                    'state': self.state,
                                    'status': 'queue',
                                    'user_order': uorder
                                })
                        # self.action_submit()
                        break

    def find_next_user(self):
        # Define logic to find the next user who should approve
        # You can use user_order or any other criteria
        print("find next ")
        next_rec = self.env['monthly.settlements.order.user.pending'].search([
            ('state', '=', self.state),
            ('monthly_settlements_id', '=', self.id),
            ('status', '=', 'queue')],
            order='user_order',
            limit=1
        )

        if next_rec:
            print("next is ", next_rec.user)
            self.show = True
            return next_rec.user
        else:
            return None

    @api.depends('current_user_id')
    def compute_show(self):
        for rec in self:
            print(f"current_user_id: {rec.current_user_id}, logged-in user: {self.env.user}")
            rec.show = rec.current_user_id == self.env.user

    def get_stages(self):
        lst = []
        rec_set = self.env['monthly.settlements.stage'].search([], order='stage_order')
        for stg in rec_set:
            lst.append((stg.code, stg.name))
        return lst

    def _get_type(self):
        ret = False
        if self.state in ('draft', 'sent', 'monthly_settlements', 'done'):
            pass
        else:
            user0 = self.env['res.users'].browse(self.env.uid)
            ret = user0.has_group('monthly_settlements_approve.monthly.settlements.stage.type')
        if ret:
            self._change_type()

    @api.model
    def create(self, vals_list):
        res = super(MonthlySettlements, self).create(vals_list)

        stages = self.env["monthly.settlements.stage.type"].search([('min_range', '=', vals_list.get('min_range'))])
        # print(stages)
        if stages:
            vals_list['current_user_to_approve'] = stages.stages.stage_users[0]
        return res



    # this is to add default text in description
    @api.model
    def default_get(self, fields):
        res = super(MonthlySettlements, self).default_get(fields)
        res['description'] = 'Per Month'
        return res

    """ 
        def compute_total_amount: 
        We used the function to check the type of amount and perform the operation according to the type
        Note: In per we must take employee_contract.wage
    """

    @api.depends('employee_name', 'amount_type', 'num_of_month', 'fixed_field', 'result')
    def compute_total_amount(self):
        for rec in self:
            rec.total_amount = 0
            if rec.amount_type == 'percentage' and rec.percentage_off == 'basic' and  rec.employee_name:
                employee_contract = self.env['hr.contract'].search([('employee_id', '=', rec.employee_name.ids),
                                                                    ('state', '=', 'open')])
                for contracts in employee_contract:

                    if employee_contract:
                        rec.total_amount = (contracts.wage * rec.percentage) / 100
            else:
                0
            # this is to check total_result if its in range or not + create fields in request view

    @api.depends('min_range', 'max_range')
    def action_submit(self):
        if self.monthly_settlements_type:
            if self.state in ('draft', 'sent'):
                print("action submit ", self.monthly_settlements_type)
                newlist = sorted(self.monthly_settlements_type.stages, key=lambda x: x.stage_order)
                print("action submit ", newlist, newlist)
                self.state = newlist[0].code
                current_stage = self.env['monthly.settlements.stage'].sudo().search([('code', '=', self.state)],
                                                                                    limit=1)
                uorder = 0
                rec_id = self.env['ir.model'].sudo().search([('model', '=', 'monthly.settlements')], limit=1)
                print("stage is ***************", current_stage)
                qquery = " select seq,res_users_id from monthly_settlements_stage_res_users_rel  where monthly_settlements_stage_id=" + str(
                    current_stage.id) + " order by seq"
                self.env.cr.execute(qquery)
                stage_users = self.env.cr.fetchall()
                print("result of query ", stage_users)
                print("sorted satge ", sorted(stage_users))
                sorted_user = sorted(stage_users)
                for user in sorted_user:
                    print("stage line in submit is ", stage_users)
                    print("user[1] submit ", user)
                    uorder = uorder + 1
                    if uorder == 1:
                        print("1 (submit)", user[1])
                        self.env['monthly.settlements.order.user.pending'].create({
                            'user': user[1],
                            'monthly_settlements_id': self.id,
                            'state': self.state,
                            'status': 'waiting',
                            'user_order': uorder
                        })
                        self.write({'current_user_id': user[1]})
                        self.env['mail.activity'].sudo().create({
                            'activity_type_id': 4,
                            'date_deadline': date.today(),
                            'summary': 'Request to approve',
                            'user_id': user[1],
                            'res_model_id': rec_id.id,
                            'res_id': self.id
                        })
                    else:
                        # print("0")
                        print("user is  (submit )", user[1], uorder)
                        self.env['monthly.settlements.order.user.pending'].create({
                            'user': user[1],
                            'monthly_settlements_id': self.id,
                            'state': self.state,
                            'status': 'queue',
                            'user_order': uorder
                        })
            else:
                print("not in range")
        else:
            stages = self.env["monthly.settlements.stage.type"].search([('min_range', '=', self.min_range)])
            if stages:
                if self.state in ('draft', 'sent'):
                    print("action submit 1  ")
                    newlist = sorted(stages.stages, key=lambda x: x.stage_order)
                    print("action submit 1  ", newlist)
                    self.state = newlist[0].code
                    print("stateee in elseee ----- :", self.state)
                    current_stage = self.env['monthly.settlements.stage'].sudo().search([('code', '=', self.state)],
                                                                                        limit=1)
                    print("current stage is ", current_stage)
                    uorder = 0
                    rec_id = self.env['ir.model'].sudo().search([('model', '=', 'monthly.settlements')], limit=1)
                    # print(rec_id)
                    qquery = " select seq,res_users_id from monthly_settlements_stage_res_users_rel  where monthly_settlements_stage_id=" + str(
                        current_stage.id) + " order by seq"
                    self.env.cr.execute(qquery)
                    stage_users = self.env.cr.fetchall()
                    for user in stage_users:
                        # print("stage line is ", stages_line)
                        # print("user[1]", user)
                        uorder = uorder + 1
                        if uorder == 1:
                            # print("1")
                            self.env['monthly.settlements.order.user.pending'].create({
                                'user': user[1],
                                'monthly_settlements_id': self.id,
                                'state': self.state,
                                'status': 'waiting',
                                'user_order': uorder
                            })
                            self.write({'current_user_id': user[1]})
                            self.env['mail.activity'].sudo().create({
                                'activity_type_id': 4,
                                'date_deadline': date.today(),
                                'summary': 'Request to approve',
                                'user_id': user[1],
                                'res_model_id': rec_id.id,
                                'res_id': self.id
                            })
                        else:
                            # print("0")
                            # print("user is ", user, uorder)
                            self.env['monthly.settlements.order.user.pending'].create({
                                'user': user[1],
                                'monthly_settlements_id': self.id,
                                'state': self.state,
                                'status': 'queue',
                                'user_order': uorder
                            })


    """ 
        def _compute_result: 
        We used the function to compute result field
    """

    @api.depends('num_of_month', 'fixed_field', 'date')
    def _compute_result(self):
        for rec in self:

            if rec.amount_type == 'percentage':
                if rec.num_of_month:
                    result = rec.total_amount / rec.num_of_month
                else:
                    result = 0
            elif rec.amount_type == 'fixed':
                result = rec.total_result / rec.num_of_month if rec.num_of_month else 0
                print("result is ", result)
            rec.result = result

    """ 
        def compute_total_result: 
        We used the function to deal with final numbers according to their type
    """

    @api.depends('amount_type', 'total_amount', 'percentage', 'fixed_field', 'total_result')
    def compute_total_result(self):
        for rec in self:
            total_result1 = 0
            if rec.amount_type == 'percentage':
                total_result1 = rec.total_amount
            elif rec.amount_type == 'fixed':
                total_result1 = rec.fixed_field
            rec.total_result = total_result1


    def action_create_record(self, ascending=True):
        # self.clicked_m_s = True
        for rec in self:
            if rec.amount_type == 'percentage':
                print("i am here percentage ")
                self.process_payslips(self.employee_name.id, ['draft', 'verify'], rec.date, rec.date)
            else:
                print("i am here ficxed ")
                self.process_payslips(self.employee_name.id, ['draft', 'verify'], rec.date, rec.date)

    def confirm(self, ascending=True):
        rec = self.env['monthly.settlements.order.user.pending'].search([
            ('user', '=', self.env.uid)
            , ('state', '=', self.state)
            , ('monthly_settlements_id', '=', self.id)
            , ('status', '=', 'waiting')
        ])
        if rec:
            oldstate = self.state
            rec.update({'status': 'approve'})
            next_user = self.find_next_user()  # Define this method to find the next user
            self.write({'current_user_id': next_user.id if next_user else False})
            for act in self.activity_ids:
                if act.activity_type_id.id == 4 and act.res_id == self.id and act.user_id.id == self.env.uid:
                    act.action_feedback('Request is approved')
            self.check_stage()
            if oldstate == self.state:
                rec_next = self.env['monthly.settlements.order.user.pending'].search([('state', '=', self.state)
                                                                                         , (
                                                                                          'monthly_settlements_id', '=',
                                                                                          self.id)
                                                                                         , ('status', '=', 'queue')]
                                                                                     , order='user_order'
                                                                                     , limit=1)
                print("rec next is--------> ", rec_next)
                if rec_next:
                    rec_next[0].update({'status': 'waiting'})
                rec_id = self.env['ir.model'].sudo().search([('model', '=', 'monthly.settlements')], limit=1)
                print(" user id in rec next is ", rec_next.user.id)
                if rec_next.user.id:
                    print("i am heeereerererererrerererer354657890-----------------------------", rec_next)
                    x = self.env['mail.activity'].sudo().create({
                        'activity_type_id': 4,
                        'date_deadline': date.today(),
                        'summary': 'Request to approve',
                        'user_id': rec_next.user.id,
                        'res_model_id': rec_id.id,
                        'res_id': self.id
                    })
                    print("rec nextttt --------", rec_next)
                if rec_next.status == False:
                    print("exxxxxxittt")

        else:
            print("no record")

    def decline(self):
        rec = self.env['monthly.settlements.order.user.pending'].search([
            ('user', '=', self.env.uid)
            , ('state', '=', self.state)
            , ('status', '=', 'waiting')
        ], limit=1)
        if rec:
            rec[0].update({'status': 'decline'})
            self.state = 'cancel'



    # def write(self, vals):
    #     for record in self:
    #         print("opeeeeeeeeeeeeeeeeeeeeeeeeeeeeerations2"
    #         )
    #         if 'monthly_settlements_lines_ids' in vals:
    #             total_amount_lines = vals.get('total_amount_lines', record.fixed_field / record.num_of_month)
    #
    #
    #             # Check if the total amount in lines exceeds the fixed_field
    #             total_amount_lines_in_lines = sum(record.monthly_settlements_lines_ids.mapped('total_amount_lines'))
    #             print("total ampunt ", total_amount_lines,total_amount_lines_in_lines,total_amount_lines_in_lines + total_amount_lines)
    #             if total_amount_lines_in_lines + total_amount_lines > record.fixed_field:
    #                 raise ValidationError(_("Total amount in lines cannot exceed fixed_field"))
    #
    #     return super(MonthlySettlements, self).write(vals)
