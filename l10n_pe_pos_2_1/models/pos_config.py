# -*- coding: utf-8 -*-

from odoo import fields, models, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    anonymous_id = fields.Many2one('res.partner', string='Anonymous Partner')
    ruc = fields.Char(related='company_id.partner_id.doc_number')
    store_sunat_code = fields.Char(related='store_id.sunat_code')
    store_street = fields.Char(related='store_id.street')
    store_authorization = fields.Char(related='store_id.authorization')
    store_name = fields.Char(related='store_id.name')
    store_phone = fields.Char(related='store_id.phone')
    store_email = fields.Char(related='store_id.email')
    store_ubigeo = fields.Char(compute='_get_store_ubigeo')
    company_ubigeo = fields.Char(compute='_get_company_ubigeo')
    company_street= fields.Char(compute='_get_company_ubigeo')

    @api.depends('store_id')
    def _get_store_ubigeo(self):
        for o in self:
            store_ubigeo = []
            if o.store_id:
                if o.store_id.district_id:
                    store_ubigeo.append(o.store_id.district_id.name.upper())
                if o.store_id.city_id:
                    store_ubigeo.append(o.store_id.city_id.name.upper())
                if o.store_id.state_id:
                    store_ubigeo.append(o.store_id.state_id.name.upper())

            o.store_ubigeo = len(store_ubigeo)>0 and " - ".join(store_ubigeo) or ''

    @api.depends('company_id')
    def _get_company_ubigeo(self):
        for o in self:
            if o.company_id:
                o.company_ubigeo = o.company_id.partner_id.get_complete_district().upper()
                o.company_street = o.company_id.street.title()
            else:
                o.company_ubigeo = o.company_id.partner_id.get_complete_district().upper()
                o.company_street = ''
