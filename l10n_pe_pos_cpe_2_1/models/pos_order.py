# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)
import base64

class AccountAccount(models.Model):
    _inherit = "account.account"

    reconcile_pos = fields.Boolean(string='No reconciliar en POS')


class PosOrder(models.Model):
    _inherit = "pos.order"

    document_type_id = fields.Many2one(
        comodel_name='sunat.document.type',
        string='Tipo de documento',
        readonly=True)
    qr_code1 = fields.Binary(string='QR',related="account_move.qr_code")
    digest_value = fields.Char(related="account_move.digest_value")
    edocument_number = fields.Char(related="account_move.edocument_number")
    afecto_amount_total = fields.Float(related="account_move.afecto_amount_total")
    exonerated_amount_total = fields.Float(related="account_move.exonerated_amount_total")
    inafecto_amount_total = fields.Float(related="account_move.inafecto_amount_total")
    igv_amount_total = fields.Float(related="account_move.igv_amount_total")
    icbper_amount_total = fields.Float(related="account_move.icbper_amount_total")
    amount_text = fields.Char(related="account_move.legend")
    id_invoice = fields.Integer(related="account_move.id")
    is_refund = fields.Boolean(string='Es una devolución', default=False)
    original_invoice_id = fields.Many2one(comodel_name='account.move',
        string='Factura origen')

    def _prepare_refund_values(self, current_session):
        res = super(PosOrder, self)._prepare_refund_values(current_session)
        res['is_refund'] = True
        if self.document_type_id and self.document_type_id.name:
            if self.document_type_id.name[0]=='B':
                res['document_type_id']=self.config_id and self.config_id.boleta_credit_note_id and self.config_id.boleta_credit_note_id.id

            elif self.document_type_id.name[0]=='F':
                res['document_type_id']=self.config_id and self.config_id.invoice_credit_note_id and self.config_id.invoice_credit_note_id.id
        if self.account_move.id:
            res['original_invoice_id']=self.account_move.id
        return res

    """
    @api.depends('account_move')
    def get_code_qr_str(self):
        for line in self:
            print(line.account_move.qr_code)
            print(type(line.account_move.qr_code))
            qr_code1 = base64.b64decode(str(line.account_move.qr_code))
            print(type(qr_code1))
            print(qr_code1)

            line.qr_code1 = qr_code1#line.account_move.qr_code
    """
    '''@api.model
    def create(self, values):
        res = super(PosOrder, self).create(values)
        
        res.action_pos_order_invoice()
        res.invoice_id.sudo().action_invoice_open()
        res.account_move = res.invoice_id.move_id
        
        return res'''

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        res['document_type_id'] = self.document_type_id.id
        print('es refundddddd', self.is_refund)
        if self.is_refund:
            catalog_9_id=self.env['catalog.9'].search([('code','=','01')],limit=1)
            if catalog_9_id:
                res['catalog_9_id']=catalog_9_id.id
                res['reversed_entry_id']=self.original_invoice_id and self.original_invoice_id.id

        return res

    @api.model
    def create_from_ui(self, orders, draft=False):
        self = self.with_context(is_pos_invoice=True)
        return super(PosOrder, self).create_from_ui(orders, draft)
    
    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)

        res['document_type_id'] = ui_order.get('document_type_id', False)
        #res['account_move'] = ui_order.get('account_move', False)
        return res

    @api.model
    def get_invoice_details(self, order):
        order_id = self.search([('pos_reference','=',order)])
        res={}
        res['digest']=order_id.account_move.digest_value or ''
        res['number']=order_id.account_move.edocument_number
        res['gravadas']=order_id.account_move.afecto_amount_total
        res['exoneradas']=order_id.account_move.exonerated_amount_total
        res['inafectas']=order_id.account_move.inafecto_amount_total
        res['igv']=order_id.account_move.igv_amount_total
        res['icbper']=order_id.account_move.icbper_amount_total
        res['id_invoice']=order_id.account_move.id
        print (res)
        return res

    @api.model
    def set_account_move(self, order):

        order_id = self.search([('id','=',order[0])])

        return order_id.account_move.id
    """

    def add_payment(self, data):
        fecha = data.get('payment_date')
        if fecha:
            fecha_pago = fields.Datetime.to_string(fields.Datetime.context_timestamp(self,fields.Datetime.from_string(fecha)))
            data['payment_date'] = fecha_pago
        return super(PosOrder, self).add_payment(data)
    def _reconcile_payments(self):
        for order in self:
            aml = order.statement_ids.mapped('journal_entry_ids') | order.account_move.line_ids | order.move_id.line_ids
            aml = aml.filtered(lambda r: not r.reconciled and r.account_id.internal_type == 'receivable' and r.partner_id == order.partner_id.commercial_partner_id and not r.account_id.reconcile_pos)

            try:
                # Cash returns will be well reconciled
                # Whereas freight returns won't be
                # "c'est la vie..."
                aml.reconcile()
            except Exception:
                # There might be unexpected situations where the automatic reconciliation won't
                # work. We don't want the user to be blocked because of this, since the automatic
                # reconciliation is introduced for convenience, not for mandatory accounting
                # reasons.
                # It may be interesting to have the Traceback logged anyway
                # for debugging and support purposes
                _logger.exception('Reconciliation did not work for order %s', order.name)
    """