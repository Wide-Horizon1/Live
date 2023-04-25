# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
import base64
from num2words import num2words
from babel.numbers import get_currency_name


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Bank Accounts')


class AccountMoveLineInh(models.Model):
    _inherit = "account.move"

    test = fields.Char('Invoice Type')
    disco = fields.Monetary('des', compute='_get_value', currency_field='currency_id', store=True)
    # sale_order_no = fields.Char(string='Sales Order No', related='sale_order_id.name', store=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', compute='_get_sale')
    partner_bank_ids = fields.Many2one('res.partner.bank', compute='_compute_partner_bank_ids',
                                       string='Partner Bank Accounts')

    total_amount_words = fields.Char('Total Price in Words', compute='_get_value')

    @api.depends('invoice_line_ids.name')
    def _get_value(self):
        for order in self:
            disc = 0
            for line in order.invoice_line_ids:
                disc += line.discount_amount_currency
            self.disco = disc

            currency_code = order.currency_id.name
            currency_symbol = order.currency_id.symbol or ''
            total_price = float(order.quick_edit_total_amount)
            total_price_words = num2words(total_price, lang='ar').title()
            currency_name = get_currency_name(currency_code, locale='ar')
            order.total_amount_words = f" فقط {total_price_words} {currency_name} لاغير "
            print("testtest..", order.total_amount_words)

            toto = self.env['res.partner.bank'].search([('partner_id', '=', order.partner_id.id)])
            print('toto', toto)

    @api.depends('name')
    def _get_sale(self):
        for rec in self:
            if rec.id:
                mm = self.env['sale.order'].search([('invoice_ids', 'in', [rec.id])])
                if mm:
                    rec.sale_order_id = mm.id
                else:
                    rec.sale_order_id = None
            else:
                rec.sale_order_id = None

    @api.depends('partner_id')
    def _compute_partner_bank_ids(self):
        for move in self:
            if len(move.partner_id.bank_ids) > 0:
                move.partner_bank_ids = move.partner_id.bank_ids[0]
            else:
                move.partner_bank_ids = False
