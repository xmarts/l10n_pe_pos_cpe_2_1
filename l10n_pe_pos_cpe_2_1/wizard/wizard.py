# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    def _default_payment_method(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            order_id = self.env['pos.order'].browse(active_id)
            if order_id.is_refund:
                original_order=self.env['pos.order'].search([('pos_reference','=',order_id.pos_reference),('is_refund','=',False)],limit=1)
                return original_order and original_order.payment_ids and original_order.payment_ids[0].payment_method_id and original_order.payment_ids[0].payment_method_id
            else:
                return order_id.session_id.payment_method_ids.sorted(lambda pm: pm.is_cash_count, reverse=True)[:1]
        return False

    payment_method_id = fields.Many2one('pos.payment.method', string='Método de pago', required=True, default=_default_payment_method)
