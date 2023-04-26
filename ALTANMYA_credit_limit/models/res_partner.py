from odoo import models, fields, api


class Partner(models.Model):
    _inherit = "res.partner"

    c_credit_limit = fields.Float(
        string='Customer Credit Limit', help='Credit limit specific to this partner.')
    c_use_partner_credit_limit = fields.Boolean(string='Partner Limit ?')
    action_type = fields.Selection(
        [('nothing', 'Do Nothing'), ('warning', 'Warning'), ('block', 'Prevent The Create Operation')],
        string='Action to execute when Exceeding the credit limit or the customer has amount due', default='nothing')
    number_of_allowed_late_days = fields.Integer('Number Of Allowed Days After Due Date')
    include_companies = fields.Boolean('Apply the action on all companies?')

    c_credit = fields.Monetary(compute='_c_credit_debit_get',
                               string='Patner Total Receivable')

    @api.depends_context('company')
    def _c_credit_debit_get(self):
        tables, where_clause, where_params = self.env['account.move.line']._where_calc([
            ('parent_state', '=', 'posted'),
        ]).get_sql()

        where_params = [tuple(self.ids)] + where_params
        if where_clause:
            where_clause = 'AND ' + where_clause
        self._cr.execute("""SELECT account_move_line.partner_id, a.account_type, SUM(account_move_line.amount_residual)
                          FROM """ + tables + """
                          LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                          WHERE a.account_type IN ('asset_receivable','liability_payable')
                          AND account_move_line.partner_id IN %s
                          AND account_move_line.reconciled IS NOT TRUE
                          """ + where_clause + """
                          GROUP BY account_move_line.partner_id, a.account_type
                          """, where_params)
        treated = self.browse()
        for pid, type, val in self._cr.fetchall():
            partner = self.browse(pid)
            if type == 'asset_receivable':
                partner.c_credit = val
                if partner not in treated:
                    treated |= partner
            elif type == 'liability_payable':
                if partner not in treated:
                    partner.c_credit = False
                    treated |= partner
        remaining = (self - treated)
        remaining.c_credit = False
        print('partner new credit ', self.c_credit)
