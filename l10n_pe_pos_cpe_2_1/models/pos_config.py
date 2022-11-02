# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_ticket = fields.Binary('Imágen Ticket')
    nro_resolucion = fields.Char('Nro. Resolución')

class PosConfig(models.Model):
    _inherit = 'pos.config'

    #invoice_journal_ids = fields.Many2many("account.journal", string="Invoice Sale Journals", domain="[('type', 'in', ['sale'])]")
    sale_ticket_id = fields.Many2one("sunat.document.type", "Ticket", domain = "[('type', '=', 'sale')]")
    sale_invoice_id = fields.Many2one("sunat.document.type", "Invoice", domain = "[('type', '=', 'sale')]")
    boleta_credit_note_id = fields.Many2one("sunat.document.type", "Nota de Crédito de boleta", domain = "[('type', '=', 'sale')]")
    invoice_credit_note_id = fields.Many2one("sunat.document.type", "Nota de Crédito de factura", domain = "[('type', '=', 'sale')]")
    is_electronic = fields.Boolean(string='Factura electrónica', related='sale_ticket_id.is_cpe')
    website = fields.Char(string='Consulta CPE', compute='_get_website')
    serie_maquina_registradora = fields.Char(string='Serie de Máquina registradora')

    def _get_website(self):
    	web = self.sudo().company_id.website
    	if web:
    		self.website = web + '/cpe'
