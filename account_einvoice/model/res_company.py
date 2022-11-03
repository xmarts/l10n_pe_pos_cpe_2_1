# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import time


class ResCompanyEinvoiceCertificate(models.Model):
    _name = 'res.company.einvoice.certificate'

    _rec_name = 'serial_number'

    company_id = fields.Many2one('res.company', string='Cliente', required=True, index=True, default=lambda self: self.env.user.company_id, help="Empresa relacionada a este certificado")
    certificate_file = fields.Binary('Archivo del certificado', filters='*.p12,*.pfx', required=True,
            help='Este archivo .cer es proporcionado por las empresas certificadas por SUNAT')
    certificate_password = fields.Char('Password del certificado', size=64, invisible=False, required=True, help='Password')
    certificate_file_pem = fields.Binary('Archivo PEM certificado', filters='*.pem,*.cer,*.certificate,*.cert', help='Este archivo es generado con el sistema basado en el certificado')
    certificate_key_file_pem = fields.Binary('Archivo PEM certificado key', filters='*.pem,*.key', help='Este archivo es generado cpor el sistema basado en el certificado')
    date_start = fields.Date('Fecha Inicio', required=False, help='Fecha de inicio del certificado')
    date_end = fields.Date('Fecha Fin', required=True, help='Fecha final de la validacion del certificado')
    serial_number = fields.Char('Numero de serie', size=64, required=True, help='Numbero de serie del certificado')
    active = fields.boolean('Active', help='Indica si el certificado es activo',  default= lambda *a: True)


class ResCompany(models.Model):
    _inherit = 'res.company'

    sunat_user = fields.Char(string='Usuario Sunat CPE', size=8, required=True, default='MODDATOS', copy=False, help='El usuario alternativo usado para el portal SUNAT con permisos de envio de compronbantes electronicos.')
    sunat_password = fields.Char(string='Contraseña Sunat CPE', invisible=True, required=True, default='MODDATOS', copy=False)
    validate_service = fields.Selection(selection=[('1','SUNAT'),('2','OSE')], string='Servicio de validación', default='1')
    osce_user = fields.Char(string='Usuario OSCE CPE', size=8, required=True, default='MODDATOS', copy=False, help='El usuario alternativo usado para el portal osce con permisos de envio de compronbantes electronicos.')
    osce_password = fields.Char(string='Contraseña OSCE CPE', invisible=True, default='MODDATOS', required=True, copy=False)
    osce_webservice = fields.Char(string='Servicio web OSCE')
    certificate_ids = fields.One2many('res.company.einvoice.certificate','company_id', string='Certificados', help='Certificados configurados en esta empresa')
    certificate_id = fields.Many2one('res.company.facturae.certificate',compute='_get_current_certificate', string='Certificado activo', help='numero de serie del certificate activo y dentro de fechas en esta empresa')

    @api.depends('certificate_ids')
    def _get_current_certificate(self):
        Certificate = self.env['res.company.einvoice.certificate']
        date = time.strftime('%Y-%m-%d')
        for company in self:
            company.certificate_id = Certificate.search([('company_id', '=', company.id),
                                                    ('date_start', '<=', date),
                                                    ('date_end', '>=', date),
                                                    ('active', '=', True)], order='date_start desc', limit=1)
