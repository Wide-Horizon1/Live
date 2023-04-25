from odoo import api, fields, models, _
from odoo.tools import formatLang

from odoo.exceptions import UserError

import datetime
import inspect


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create([self._sanitize_vals(vals) for vals in vals_list])
        partner = moves.partner_id.commercial_partner_id
        moves.compute_partner_late_payment()
        print('anas')
        save = False
        try:
            print('pa', partner.c_use_partner_credit_limit)
            if partner.c_use_partner_credit_limit:
                print(partner.c_credit_limit, partner.credit, moves.amount_total)
                print('partner.credit ', partner.credit)
                if partner.c_credit_limit < partner.credit + moves.amount_total:
                    if partner.action_type == 'nothing':
                        pass
                    elif partner.action_type == 'block':
                        print('partner company id',  partner.company_id.id)
                        print('move company id',  moves.company_id.id)
                        # if not partner.include_companies and moves.company_id.id == self.env.company.id:
                        print('ll')
                        save = True
                        raise UserError(
                            f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')
                        # elif partner.include_companies:
                        #     save = True
                        #     raise UserError(
                        #         f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')
        finally:
            print('fina move 2', save)
            if save:
                amount_total = moves.amount_total
                self.env.cr.rollback()
                self.create_prevention_log_rec(partner,
                                               'the customer has reached his Credit Limit', amount_total)

        try:
            if moves.compute_partner_late_payment():
                if partner.action_type == 'nothing':
                    pass
                elif partner.action_type == 'block':
                    print('mm')
                    save = True
                    raise UserError(
                        f'{partner.name} has unpaid invoices and the payment deadline is over')
        finally:
            print('fina move', save)
            if save:
                amount_total = moves.amount_total
                self.env.cr.rollback()
                self.create_prevention_log_rec(partner,
                                               'the customer has unpaid invoices and the payment deadline is over',
                                               amount_total)
        return moves

    def action_post(self):
        moves_with_payments = self.filtered('payment_id')
        other_moves = self - moves_with_payments
        partner = self.partner_id.commercial_partner_id
        if partner.c_use_partner_credit_limit:
            print(partner.c_credit_limit, partner.credit, self.amount_total)
            if partner.c_credit_limit < partner.credit + self.amount_total:
                print('partner.c_credit_limit : ', partner.c_credit_limit)
                print('partner.credit : ', partner.credit)
                print('amount_total : ', self.amount_total)
                if partner.action_type == 'nothing':
                    pass
                elif partner.action_type == 'block':
                    # if not partner.include_companies and partner.company_id.id == self.company_id.id:
                    self.create_prevention_log_rec(partner,
                                                   'the customer has reached his Credit Limit', self.amount_total)
                    raise UserError(
                        f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')

        if moves_with_payments:
            moves_with_payments.payment_id.action_post()
        if other_moves:
            other_moves._post(soft=False)
        return False

    # def write(self, vals):
    #     moves = super().write(vals)
    #     print('vals in cre lim : ', vals, moves, self.partner_id)
    #     partner_id = vals.get('partner_id') if vals.get('partner_id') is not None else self.partner_id
    #     if type(partner_id) == type(self.id):
    #         partner_id = self.env['res.partner'].search([('id', '=', partner_id)])
    #     amount_total = vals.get('amount_total') if vals.get('amount_total') is not None else self.amount_total
    #     partner = partner_id.commercial_partner_id
    #     # if vals.get(''):
    #     if partner.c_use_partner_credit_limit:
    #         print(partner.c_credit_limit, partner.credit, amount_total)
    #         if partner.c_credit_limit < partner.credit + amount_total:
    #             print('partner.c_credit_limit : ', partner.c_credit_limit)
    #             print('partner.credit : ', partner.credit)
    #             print('amount_total : ', amount_total)
    #             if partner.action_type == 'nothing':
    #                 pass
    #             elif partner.action_type == 'block':
    #                 # if not partner.include_companies and partner.company_id.id == self.company_id.id:
    #                 self.create_prevention_log_rec(partner,
    #                                                'the customer has reached his Credit Limit', self.amount_total)
    #                 raise UserError(
    #                     f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')
    #         # elif partner.include_companies:
    #         #     self.create_prevention_log_rec(partner,
    #         #                                    'the customer has reached his Credit Limit', self.amount_total)
    #         #     raise UserError(
    #         #         f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')
    #     return moves

    def _build_credit_warning_message(self, record, updated_credit):
        ''' Build the warning message that will be displayed in a yellow banner on top of the current record
            if the partner exceeds a credit limit (set on the company or the partner itself).
            :param record:                  The record where the warning will appear (Invoice, Sales Order...).
            :param updated_credit (float):  The partner's updated credit limit including the current record.
            :return (str):                  The warning message to be showed.
        '''
        partner_id = record.partner_id.commercial_partner_id
        print('record in build : ', record)
        msg = ''
        if record.compute_partner_late_payment():
            msg += f'{partner_id.name} has unpaid invoices and the payment deadline is over\n'
        if not partner_id.c_credit_limit or updated_credit <= partner_id.c_credit_limit:
            return msg
        msg += _('%s has reached its Credit Limit of : %s\nTotal amount due ',
                 partner_id.name,
                 formatLang(self.env, partner_id.c_credit_limit, currency_obj=record.company_id.currency_id))
        if updated_credit > partner_id.credit:
            msg += _('(including this document) ')
        msg += ': %s' % formatLang(self.env, updated_credit, currency_obj=record.company_id.currency_id)
        return msg

    def compute_partner_late_payment(self):
        print('partner : ', self.partner_id)
        print('now : ', fields.Datetime.now(), self.partner_id.commercial_partner_id.number_of_allowed_late_days)
        print('long ', fields.Datetime.now() - datetime.timedelta(
            days=self.partner_id.commercial_partner_id.number_of_allowed_late_days))
        move_id = self.id if self.id else -1
        print('include ', self.partner_id.include_companies)
        if self.partner_id.include_companies:
            query = f"""
            SELECT id
            FROM account_move
            WHERE partner_id = {self.partner_id.id}
            AND invoice_date_due < '{fields.Datetime.now() - datetime.timedelta(
                days=self.partner_id.commercial_partner_id.number_of_allowed_late_days)}'
            AND state = 'posted'
            AND id != {move_id}
            """
            domain = [('partner_id', '=', self.partner_id.id),
                      ('invoice_date_due', '<', fields.Datetime.now() - datetime.timedelta(
                          days=self.partner_id.commercial_partner_id.number_of_allowed_late_days)),
                      ('state', '=', 'posted'), ('id', '!=', move_id)]
        else:
            query = f"""
                        SELECT id
                        FROM account_move
                        WHERE partner_id = {self.partner_id.id}
                        AND invoice_date_due < '{fields.Datetime.now() - datetime.timedelta(
                days=self.partner_id.commercial_partner_id.number_of_allowed_late_days)}'
                        AND state = 'posted'
                        AND id != {move_id}
                        AND company_id = {self.company_id.id}
                        """
            domain = [('partner_id', '=', self.partner_id.id),
                      ('invoice_date_due', '<', fields.Datetime.now() - datetime.timedelta(
                          days=self.partner_id.commercial_partner_id.number_of_allowed_late_days)),
                      ('state', '=', 'posted'), ('id', '!=', move_id), ('company_id', '=', self.company_id.id)]
        if self.partner_id:
            print('all invoices', self.env['account.move'].search([('company_id', '!=', None)]))
            # late_invoices = self.env['account.move'].search(domain)
            self.env.cr.execute(query)
            late_invoices = self.env.cr.fetchall()
            print('late invoices "move" : ', late_invoices)
            if len(late_invoices) >= 1:
                return True
            else:
                return False

    @api.depends('company_id', 'partner_id', 'tax_totals', 'currency_id')
    def _compute_partner_credit_warning(self):
        for move in self:
            move.with_company(move.company_id)
            move.partner_credit_warning = ''
            show_warning = move.state == 'draft' and \
                           move.move_type == 'out_invoice' and \
                           move.company_id.account_use_credit_limit
            if self.partner_id.action_type == 'warning':
                amount_total_currency = move.currency_id._convert(move.tax_totals['amount_total'],
                                                                  move.company_currency_id, move.company_id, move.date)
                updated_credit = move.partner_id.commercial_partner_id.credit + amount_total_currency
                move.partner_credit_warning = self._build_credit_warning_message(move, updated_credit)

    def create_prevention_log_rec(self, partner, reason, amount):
        print('re', reason)
        rec = self.env['partner.prevention.log'].sudo().create({
            'partner_id': partner.id,
            'prevention_date': fields.Datetime.now(),
            'so_invoice': 'invoice',
            'reason': reason,
            'amount': amount
        })
        self.env.cr.commit()
        print('rec : ', rec)
