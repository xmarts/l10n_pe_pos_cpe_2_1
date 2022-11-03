# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
import requests

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def get_partner_from_ui(self, doc_type, doc_number):
        #url=None
        res={}
        '''if doc_type=="1":
            res = self.get_data_partner_dni(doc_number)'''
        if doc_type=="6":
            res = self.get_data_partner_ruc(doc_number)
            print(res)
            #{'error': False, 'error_msg': None, 
            #'data': {'tipo_contribuyente': 'SOCIEDAD ANONIMA CERRADA', 'nombre_comercial': '-', 
            #'domicilio_fiscal': 'Pasaje Eolo 285', 'fecha_inscripcion': '2017-11-13', 
            #'razon_social': 'RAPID TECHNOLOGIES S.A.C.', 'numero_documento': '20602623433', 
            #'condicion_contribuyente': 'HABIDO', 'estado_contribuyente': 'ACTIVO', 'ubigeo': 'PE150115'}}
            if res['error'] == False:
                if res['data']['ubigeo']:
                    district = self.env['l10n_pe.res.city.district'].search([('code','=',res['data']['ubigeo'][2:])],limit=1)
                    if district:
                        res['data']['l10n_pe_district'] = district.id
                        res['data']['city_id']=district.city_id and district.city_id.id
                        res['data']['state_id'] = district.city_id and district.city_id.state_id and district.city_id.state_id.id

        return res
    
    @api.model
    def create_from_ui(self, partner):
        if partner.get("doc_type"):
            doc_type = self.env['table.ple.2'].search([('id','=',partner.get("doc_type"))])
            if doc_type.code=="6":
                partner['is_company']=True
        print('PARTNEEERR', partner)
        return super(ResPartner, self).create_from_ui(partner)