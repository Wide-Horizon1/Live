# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
import base64
from num2words import num2words
from babel.numbers import get_currency_name
from itertools import groupby


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Bank Accounts')


class AccountMoveLineInh(models.Model):
    _inherit = "account.move"

    test = fields.Char('Invoice Type')
    disco = fields.Monetary('des', compute='_get_valueeee', currency_field='currency_id', store=True)

    # sale_order_no = fields.Char(string='Sales Order No', related='sale_order_id.name', store=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', compute='_get_sale')
    partner_bank_ids = fields.Many2one('res.partner.bank', compute='_compute_partner_bank_ids',
                                       string='Partner Bank Accounts')

    total_amount_words = fields.Char('Total Price in Words', compute='_get_value')

    @api.depends('invoice_line_ids.name', 'currency_id')
    def _get_valueeee(self):
        for currency, records in groupby(self, lambda r: r.currency_id):
            for record in records:
                if record.invoice_line_ids:
                    total_disc = record._compute_disc()
                    record.disco = total_disc
                    print("descoesco", total_disc)

    def _compute_disc(self):
        return sum(line.result for line in self.invoice_line_ids)

    @api.depends('invoice_line_ids.name')
    def _get_value(self):
        for order in self:
            if order.currency_id:
                currency_code = order.currency_id.name
                currency_symbol = order.currency_id.symbol or ''
                total_price = float(order.amount_total_signed)
                total_price_words = num2words(total_price, lang='ar').title()
                currency_name = get_currency_name(currency_code, locale='ar')
                order.total_amount_words = f" فقط {total_price_words} {currency_name} لاغير "
                print("testtest..", order.total_amount_words)

    # @api.depends('name','partner_id','invoice_line_ids.name')
    # def _get_sale(self):
    #     for rec in self:
    #         print('recrecrec',rec)
    #         print('recrecrec222', rec.id)
    #         if rec and rec.id:
    #             print('recrecrec222',rec.id)
    #             mm = self.env['sale.order'].search([('invoice_ids', 'in', [rec.id])])
    #             if mm:
    #                 rec.sale_order_id = mm.id
    #             else:
    #                 rec.sale_order_id = False
    #         else:
    #             rec.sale_order_id = False

    @api.depends('name','invoice_origin')
    def _get_sale(self):
        for rec in self:
            print('recrecrec', rec)
            if rec.invoice_origin:
                sale_order = self.env['sale.order'].search([('name', '=', rec.invoice_origin)], limit=1)
                if sale_order:
                    rec.sale_order_id = sale_order.id
                else:
                    rec.sale_order_id = False
            else:
                rec.sale_order_id = False

    @api.depends('partner_id')
    def _compute_partner_bank_ids(self):
        for move in self:
            if move.partner_id and len(move.partner_id.bank_ids) > 0:
                move.partner_bank_ids = move.partner_id.bank_ids[0]
            else:
                move.partner_bank_ids = False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    result = fields.Float(string='Discount Amount', compute='_compute_result', store=True, readonly=True)

    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_result(self):
        for line in self:
            if line.quantity and line.price_unit and line.discount:
                line.result = line.quantity * line.price_unit * (line.discount / 100)
            else:
                line.result = 0.0
