# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


UNIDADES = (
    '',
    'UN ',
    'DOS ',
    'TRES ',
    'CUATRO ',
    'CINCO ',
    'SEIS ',
    'SIETE ',
    'OCHO ',
    'NUEVE ',
    'DIEZ ',
    'ONCE ',
    'DOCE ',
    'TRECE ',
    'CATORCE ',
    'QUINCE ',
    'DIECISEIS ',
    'DIECISIETE ',
    'DIECIOCHO ',
    'DIECINUEVE ',
    'VEINTE '
)
DECENAS = (
    'VEINTI',
    'TREINTA ',
    'CUARENTA ',
    'CINCUENTA ',
    'SESENTA ',
    'SETENTA ',
    'OCHENTA ',
    'NOVENTA ',
    'CIEN '
)
CENTENAS = (
    'CIENTO ',
    'DOSCIENTOS ',
    'TRESCIENTOS ',
    'CUATROCIENTOS ',
    'QUINIENTOS ',
    'SEISCIENTOS ',
    'SETECIENTOS ',
    'OCHOCIENTOS ',
    'NOVECIENTOS '
)


def Numero_a_Texto(number_in):

    converted = ''

    if type(number_in) != 'str':
        number = str(number_in)
    else:
        number = number_in

    number_str = number

    try:
        number_int, number_dec = number_str.split(".")
    except ValueError:
        number_int = number_str
        number_dec = ""

    number_str = number_int.zfill(9)
    millones = number_str[:3]
    miles = number_str[3:6]
    cientos = number_str[6:]

    if(millones):
        if(millones == '001'):
            converted += 'UN MILLON '
        elif(int(millones) > 0):
            converted += '%sMILLONES ' % __convertNumber(millones)

    if(miles):
        if(miles == '001'):
            converted += 'UN MIL '
        elif(int(miles) > 0):
            converted += '%sMIL ' % __convertNumber(miles)
    if(cientos):
        if(cientos == '001'):
            converted += 'UN '
        elif(int(cientos) > 0):
            converted += '%s ' % __convertNumber(cientos)

    if number_dec == "":
        number_dec = "00"
    if (len(number_dec) < 2):
        number_dec += '0'

    converted += 'CON ' + number_dec + "/100"

    return converted


def __convertNumber(n):
    output = ''

    if(n == '100'):
        output = "CIEN "
    elif(n[0] != '0'):
        output = CENTENAS[int(n[0]) - 1]

    k = int(n[1:])
    if(k <= 20):
        output += UNIDADES[k]
    else:
        if((k > 30) & (n[2] != '0')):
            output += '%sY %s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
        else:
            output += '%s%s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])

    return output


class Catalog7(models.Model):
    _name = 'catalog.7'
    _description='Catálogo 7'

    code = fields.Char('Código')
    name = fields.Char('Nombre')
    description = fields.Text('Descripción')


class Catalog8(models.Model):
    _name = 'catalog.8'
    _description='Catálogo 8'

    code = fields.Char('Código')
    name = fields.Char('Descripción')


class Catalog9(models.Model):
    _name = 'catalog.9'
    _description='Catálogo 9'

    code = fields.Char('Código')
    name = fields.Char('Descripción')


class Catalog10(models.Model):
    _name = 'catalog.10'
    _description='Catálogo 10'

    code = fields.Char('Código')
    name = fields.Char('Descripción')

class Catalog15(models.Model):
    _name = 'catalog.15'
    _description='Catálogo 15'

    code = fields.Char('Código')
    name = fields.Char('Descripción')

class Catalog16(models.Model):
    _name = 'catalog.16'
    _description='Catálogo 16'

    code = fields.Char('Código')
    name = fields.Char('Descripción')
    
class AccountTax(models.Model):
    _inherit = 'account.tax'
    
    is_igv = fields.Boolean('Es IGV', default=False)
    catalog_7_id = fields.Many2one(
        comodel_name='catalog.7', string='Tipo de afectación al IGV')
    is_isc = fields.Boolean('Es ISC', default=False)
    catalog_8_id = fields.Many2one(
        comodel_name='catalog.8', string='Tipo de Sistema de Cálculo del ISC')


class AccountMove(models.Model):
    _inherit = "account.move"
    
    document_type_id = fields.Many2one(
        comodel_name='sunat.document.type',
        string='Tipo de documento',
        domain="[('visible_document','=','factura')]",
        readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    edocument_number = fields.Char(string='Nro. de comprobante', readonly=True, copy=False)
    type_journal = fields.Char(
        compute='_get_type_document',
        string='Código de tipo de comprobante',
        store=True)
    inafecto_amount_total = fields.Float(
        compute='_get_inafecto_total',
        digits='Account',
        string='Monto total operaciones inafectas',
        store=True)
    exonerated_amount_total = fields.Float(
        compute='_get_exonerated_total',
        digits='Account',
        string='Monto total operaciones exoneradas',
        store=True)
    afecto_amount_total = fields.Float(
        compute='_get_afecto_total',
        digits='Account',
        string='Monto total operaciones gravadas',
        store=True)
    ono_amount_total = fields.Float(
        compute='_get_ono_amount_total',
        digits='Account',
        string='Monto total operaciones gratuitas',
        store=True)
    igv_amount_total = fields.Float(
        compute='_get_igv_total',
        digits='Account',
        string='Sumatoria Total IGV',
        store=True)
    isc_amount_total = fields.Float(
        compute='_get_isc_total',
        digits='Account',
        string='Sumatoria total ISC',
        store=True)
    othertaxes_amount_total = fields.Float(
        compute='_get_othertaxes_total',
        digits='Account',
        string='Sumatoria total otros impuestos',
        store=True)
    othercharges_amount_total = fields.Float(
        string='Sumatoria otros cargos',
        digits='Account', default=0.00)
    discount_amount_total = fields.Float(
        compute='_get_discount_total',
        digits='Account',
        string='Total descuento', store=True)
    global_discount = fields.Float(
        string='Descuentos globales',
        digits='Account',
        default=0.00,
        help='Porcentaje de descuento global, si es 5% colocar 5')
    catalog_9_id = fields.Many2one(
        comodel_name='catalog.9',
        string='Tipo de nota de crédito')
    type_origin = fields.Char(
        compute='_get_type_origin',
        string='Tipo de documento origen',
        default=False,
        store=True)
    catalog_10_id = fields.Many2one(
        comodel_name='catalog.10', string='Tipo de nota de debito')
    legend = fields.Char(compute='_get_legend', string='Leyenda')
    code_legend = fields.Char(compute='_get_legend', string='Codigo leyenda')
    catalog_15 = fields.Char(
        compute='_get_catalog_15', string='Códigos elementos adicionales')
    #procesado = fields.Boolean('Comprobante Procesado')
    #status_einvoice = fields.Char('Estado del comprobante')
    #rvalue = fields.Char('Valor resumen de la respuesta SUNAT')
    #digest_value = fields.Char('Valor resumen del comprobante')
    is_boleta = fields.Boolean(compute='_get_boleta', default=False, store=True)
    is_debit_note = fields.Boolean(compute='_get_debit_note', default=False, store=True)
    is_credit_note = fields.Boolean(compute='_get_credit_note', default=False, store=True)
    supplier_proof_series = fields.Char(
            string='Serie del comprobante',
            size=20, readonly=True,
            states={'draft': [('readonly', False)]})
    supplier_proof_number = fields.Char(
            string='Número del comprobante',
            size=20, readonly=True,
            states={'draft': [('readonly', False)]})
    supplier_invoice_number = fields.Char(
            compute='_get_supplier_invoice_number',
            string='Supplier Invoice Number',
            help="The reference of this invoice as provided by the supplier.",
            readonly=True, store=True,
            states={'draft': [('readonly', False)]})
    sunat_code_purchase = fields.Many2one(comodel_name='table.ple.10', string = 'Tipo de comprobante de pago proveedor')
    invoice_reference_id = fields.Many2one('account.move','Documento de Referencia ND') 
    glosa = fields.Char(string='Glosa')

    @api.onchange('date', 'currency_id', 'invoice_date')
    def _onchange_currency(self):
        currency = self.currency_id or self.company_id.currency_id
        date_ant=False
        if self.is_invoice(include_receipts=True):
            date_ant = self.date
            self.date=self.invoice_date
            for line in self._get_lines_onchange_currency():
                line.currency_id = currency
                line._onchange_currency()
        else:
            for line in self.line_ids:
                line._onchange_currency()

        self._recompute_dynamic_lines(recompute_tax_base_amount=True)
        if date_ant:
            self.date=date_ant

    @api.constrains('name', 'journal_id', 'state','document_type_id')
    def _check_unique_sequence_number(self):
        moves = self.filtered(lambda move: move.state == 'posted')
        if not moves:
            return

        self.flush()

        # /!\ Computed stored fields are not yet inside the database.
        self._cr.execute('''
            SELECT move2.id, move2.name
            FROM account_move move
            INNER JOIN account_move move2 ON
                move2.name = move.name
                AND move2.journal_id = move.journal_id
                AND move2.move_type = move.move_type
                AND move2.document_type_id = move.document_type_id
                AND move2.id != move.id
            WHERE move.id IN %s AND move2.state = 'posted'
        ''', [tuple(moves.ids)])
        res = self._cr.fetchall()
        if res:
            raise ValidationError(_('Posted journal entry must have an unique sequence number per company.\n'
                                    'Problematic numbers: %s\n') % ', '.join(r[1] for r in res))

    '''@api.model
    def create(self, values):
        if values.get('partner_id'):
            if not values.get('document_type_id'):
                partner_id = self.env['res.partner'].search([('id','=',values.get('partner_id'))])
                if partner_id and partner_id.doc_type and partner_id.doc_type.code and values.get('type') == 'out_invoice':
                    if partner_id.doc_type.code=='6':
                        default_facturas = self.env['sunat.document.type'].search([('factura_default','=',True)])
                        if default_facturas:
                            values['document_type_id'] = default_facturas[0].id
                    else:
                        default_boletas = self.env['sunat.document.type'].search([('boleta_default','=',True)])
                        if default_boletas:
                            values['document_type_id'] = default_boletas[0].id
                elif partner_id and partner_id.doc_type and partner_id.doc_type.code and values.get('type') == 'out_refund':
                    if partner_id.doc_type.code=='6':
                        default_facturas = self.env['sunat.document.type'].search([('nc_factura_default','=',True)])
                        if default_facturas:
                            values['document_type_id'] = default_facturas[0].id
                    else:
                        default_boletas = self.env['sunat.document.type'].search([('nc_boleta_default','=',True)])
                        if default_boletas:
                            values['document_type_id'] = default_boletas[0].id
        return super(AccountMove, self).create(values)'''

    
    @api.depends('supplier_proof_series', 'supplier_proof_number')
    def _get_supplier_invoice_number(self):
        for invoice in self:
            if invoice.move_type == "in_invoice":
                if invoice.supplier_proof_series and invoice.supplier_proof_number:
                    invoice.supplier_invoice_number = \
                        invoice.supplier_proof_series + \
                        '-' + invoice.supplier_proof_number

    @api.depends('document_type_id')
    def _get_boleta(self):
        for invoice in self:
            if invoice.document_type_id.sunat_code.code == '03':
                invoice.is_boleta = True
            else:
                invoice.is_boleta = False

    @api.depends('document_type_id')
    def _get_debit_note(self):
        for invoice in self:
            if invoice.document_type_id.sunat_code.code == '08':
                invoice.is_debit_note = True
            else:
                invoice.is_debit_note = False
    
    @api.depends('document_type_id')
    def _get_credit_note(self):
        for invoice in self:
            if invoice.document_type_id.sunat_code.code == '07':
                invoice.is_credit_note = True
            else:
                invoice.is_credit_note = False


    '''@api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'global_discount', 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        self.ensure_one()
        round_curr = self.currency_id.round
        self.amount_untaxed = sum(
            line.price_subtotal for line in self.invoice_line_ids) * \
                (1-self.global_discount/100)
        self.amount_tax = sum(
            round_curr(line.amount) for line in self.tax_line_ids) * \
                (1-self.global_discount/100)
        self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id
            amount_total_company_signed = currency_id._convert(self.amount_total, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
            amount_untaxed_signed = currency_id._convert(self.amount_untaxed, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
        sign = self.move_type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign'''

    @api.depends('document_type_id')
    def _get_type_document(self):
        for invoice in self:
            if invoice.document_type_id:
                invoice.type_journal = invoice.document_type_id.sunat_code.code \
                    if invoice.document_type_id.sunat_code.code else False
            else:
                invoice.type_journal=False

    @api.depends('reversed_entry_id')
    def _get_type_origin(self):
        for invoice in self:
            if invoice.reversed_entry_id:
                invoice.type_origin = invoice.reversed_entry_id and invoice.reversed_entry_id.document_type_id and invoice.reversed_entry_id.document_type_id.sunat_code.code
            else:
                invoice.type_origin = False

    @api.depends('invoice_line_ids.price_subtotal','global_discount')
    def _get_inafecto_total(self):
        for invoice in self:
            invoice.inafecto_amount_total = 0.00
            for line in invoice.invoice_line_ids:
                if line.igv_sale_code in \
                   ['30', '31', '32', '33', '34', '35', '36']:
                    invoice.inafecto_amount_total += line.price_subtotal
            invoice.inafecto_amount_total = invoice.inafecto_amount_total*(1-invoice.global_discount/100)

    @api.depends('invoice_line_ids.price_subtotal', 'global_discount')
    def _get_exonerated_total(self):
        for invoice in self:
            invoice.exonerated_amount_total = 0.00
            for line in invoice.invoice_line_ids:
                if line.igv_sale_code == '20':
                    invoice.exonerated_amount_total += line.price_subtotal
            invoice.exonerated_amount_total = invoice.exonerated_amount_total * (1-invoice.global_discount/100)

    @api.depends(
        'amount_untaxed',
        'inafecto_amount_total',
        'exonerated_amount_total')
    def _get_afecto_total(self):
        for invoice in self:
            invoice.afecto_amount_total = invoice.amount_untaxed \
                - invoice.inafecto_amount_total \
                - invoice.exonerated_amount_total

    @api.depends('invoice_line_ids.ono_amount_subtotal')
    def _get_ono_amount_total(self):
        for invoice in self:
            invoice.ono_amount_total = 0.00
            for line in invoice.invoice_line_ids:
                if line.ono_amount_subtotal:
                    invoice.ono_amount_total += line.ono_amount_subtotal

    @api.depends('ono_amount_total')
    def _get_catalog_15(self):
        for invoice in self:
            if invoice.ono_amount_total == 0:
                invoice.catalog_15 = '1000'
            else:
                invoice.catalog_15 = '1002'

    @api.depends('amount_total', 'ono_amount_total')
    def _get_legend(self):
        for invoice in self:
            if invoice.amount_total > 0 or (invoice.amount_total==0 and invoice.is_has_advance):
                invoice.code_legend = '1000'
                if invoice.currency_id.long_name:
                    invoice.legend = Numero_a_Texto(
                        invoice.amount_total) + ' ' + invoice.currency_id.long_name
                else:
                    invoice.legend = Numero_a_Texto(invoice.amount_total)
            else:
                invoice.code_legend = '1002'
                invoice.legend = 'TRANSFERENCIA GRATUITA DE UN BIEN Y/O SERVICIO PRESTADO GRATUITAMENTE'

    @api.depends('invoice_line_ids.igv_sale_value', 'global_discount')
    def _get_igv_total(self):
        for invoice in self:
            invoice.igv_amount_total = 0.00
            for line in invoice.invoice_line_ids:
                invoice.igv_amount_total += line.igv_sale_value
            invoice.igv_amount_total = invoice.igv_amount_total * (1-invoice.global_discount/100)

    @api.depends('invoice_line_ids.isc_sale_value', 'global_discount')
    def _get_isc_total(self):
        for invoice in self:
            invoice.isc_amount_total = 0.00
            for line in invoice.invoice_line_ids:
                invoice.isc_amount_total += line.isc_sale_value
            invoice.isc_amount_total = invoice.isc_amount_total * (1-invoice.global_discount/100)

    @api.depends('invoice_line_ids')
    def _get_othertaxes_total(self):
        for invoice in self:
            invoice.othertaxes_amount_total = 0.0

    @api.depends('invoice_line_ids.amount_item_discount', 'global_discount')
    def _get_discount_total(self):
        for invoice in self:
            invoice.discount_amount_total = 0.00
            for line in invoice.invoice_line_ids:
                invoice.discount_amount_total += line.amount_item_discount + \
                    (line.price_subtotal + line.igv_sale_value + line.isc_sale_value) * \
                    invoice.global_discount/100


    def _post(self, soft=True):
        for invoice in self:
            if invoice.move_type in ['out_invoice','out_refund'] and not invoice.document_type_id:
                raise UserError('Es necesario seleccionar un tipo de documento')
            if invoice.move_type in ['out_invoice','out_refund']:
                if invoice.edocument_number:
                    invoice.name = invoice.edocument_number
                else:
                    invoice.name = invoice.document_type_id._get_number_of_document()
                    invoice.edocument_number = invoice.name
                    invoice.document_type_id._set_next_number()
        new_id = super(AccountMove, self)._post(soft=True)
        return new_id   


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    reference_value_unit = fields.Float(
        string='valor referencial O.N.O.', default=0.00)
    unit_value_fe = fields.Float(compute='_get_unit_value', digits='Product Price', string='Valor unitario', store=True)
    item_discount_indicator = fields.Boolean(
        default=False, compute='_get_discount_indicator', string='Indicador descuento por item', store=True)
    amount_item_discount = fields.Float(compute='_get_amount_discount', string='Monto descuento por item', store=True)
    igv_sale_value = fields.Float(compute='_get_igv_sale_value', digits=(12,2), string='Monto IGV por linea', store=True)
    igv_sale_code = fields.Char(
        compute='_get_igv_sale_code', string='Código afectación al IGV', store=True)
    isc_sale_value = fields.Float(compute='_get_isc_sale_value', digits=(12,2), string='Monto ISC por linea', store=True)
    isc_sale_code = fields.Char(
        compute='_get_isc_sale_code', string='Tasa asociada al ítem en concreto', store=True)
    unit_sale_price = fields.Float(compute='_get_unit_sale_price', digits='Product Price', string='Precio de venta unitario', store=True)
    ono_amount_subtotal = fields.Float(compute='_get_ono_subtotal', string='Subtotal operaciones no onerosas', store=True)
    price_type_code = fields.Char(compute='_get_price_type_code', string='Codigo tipo de precio', store=True)
    glosa = fields.Char(string='Glosa', related='move_id.glosa', store=True)

    @api.depends('price_subtotal', 'discount', 'quantity')
    def _get_unit_value(self):
        for invoice in self:
            invoice.unit_value_fe = invoice.price_subtotal / \
                invoice.quantity if invoice.quantity != 0.00 and invoice.discount != 100 else 0.00

    
    @api.depends('discount')
    def _get_discount_indicator(self):
        for invoice in self:
            if invoice.discount == 0.00:
                invoice.item_discount_indicator = True
            else:
                invoice.item_discount_indicator = False

    @api.depends('unit_value_fe', 'quantity', 'discount')
    def _get_amount_discount(self):
        for invoice in self:
            invoice.amount_item_discount = invoice.unit_value_fe * invoice.quantity * \
                (invoice.discount / 100) if invoice.discount else 0.00

    @api.depends('tax_ids', 'price_unit', 'discount', 'quantity')
    def _get_igv_sale_value(self):
        for invoice in self:
            if invoice.tax_ids:
                tax_igv_id = None
                for taxes in invoice.tax_ids:
                    if taxes.catalog_7_id:
                        tax_igv_id = taxes
                tax_amount = 0.00
                if tax_igv_id:
                    if invoice.move_id:
                        currency = invoice.move_id.currency_id
                        partner = invoice.move_id.partner_id
                    price_unit = invoice.price_unit * (1 - (invoice.discount or 0.0) / 100.0)
                    for tax in invoice.tax_ids.compute_all(price_unit,currency, invoice.quantity, invoice.product_id,partner)['taxes']:
                        if tax['id'] == tax_igv_id.id:
                            tax_amount += tax['amount']
                    invoice.igv_sale_value = tax_amount
            else:
                invoice.igv_sale_value = 0.00

    @api.depends('tax_ids', 'price_unit', 'discount', 'quantity')
    def _get_isc_sale_value(self):
        for invoice in self:
            if invoice.tax_ids:
                tax_isc_id = None
                for taxes in invoice.tax_ids:
                    if taxes.is_isc == True:
                        tax_isc_id = taxes
                tax_amount = 0.00
                if tax_isc_id:
                    if invoice.move_id:
                        currency = invoice.move_id.currency_id
                        partner = invoice.move_id.partner_id
                    price_unit = invoice.price_unit * (1 - (invoice.discount or 0.0) / 100.0)
                    for tax in invoice.tax_ids.compute_all(price_unit,currency, invoice.quantity, invoice.product_id,partner)['taxes']:
                        if tax['id'] == tax_isc_id.id:
                            tax_amount += tax['amount']
                    invoice.isc_sale_value = tax_amount
            else:
                invoice.isc_sale_value = 0.00

    @api.depends('price_subtotal', 'igv_sale_value', 'isc_sale_value', 'quantity')
    def _get_unit_sale_price(self):
        for invoice in self:
            invoice.unit_sale_price = (invoice.price_subtotal + invoice.igv_sale_value +
                                    invoice.isc_sale_value) / invoice.quantity if invoice.quantity != 0.00 else 0.00

    @api.depends('tax_ids')
    def _get_igv_sale_code(self):
        for invoice in self:
            if invoice.tax_ids:
                for tax in invoice.tax_ids:
                    if tax.catalog_7_id:
                        invoice.igv_sale_code = tax.catalog_7_id.code

    @api.depends('tax_ids')
    def _get_isc_sale_code(self):
        for invoice in self:
            if invoice.tax_ids:
                for tax in invoice.tax_ids:
                    if tax.catalog_8_id:
                        invoice.isc_sale_code = tax.catalog_8_id.code

    @api.depends('reference_value_unit')
    def _get_ono_subtotal(self):
        for invoice in self:
            invoice.ono_amount_subtotal = 0.00
            if invoice.reference_value_unit != 0:
                invoice.ono_amount_subtotal = invoice.quantity * invoice.reference_value_unit
            
    @api.depends('reference_value_unit')
    def _get_price_type_code(self):
        for invoice in self:
            if invoice.reference_value_unit:
                invoice.price_type_code = '02'
            else:
                invoice.price_type_code = '01'

    '''@api.model
    def create(self, values):
        new_id = super(AccountMoveLine, self).create(values)
        invoice = new_id.move_id
        sequence = 0
        account_invoice_line_obj = invoice.invoice_line_ids
        for line in account_invoice_line_obj:
            sequence += 1
            line.write({'secuencia': sequence})
        return new_id'''

class TablePle10(models.Model):
    _inherit = 'table.ple.10'

    move_type = fields.Selection([
        ('entry','Asiento contable'),
        ('out_invoice','Comprobante de Pago'),
        ('out_refund','Nota de Crédito de cliente'),
        ('in_invoice','Factura de proveedor'),
        ('in_refund','Factura rectificativa de proveedor'),
        ('out_receipt','Recibo de ventas'),
        ('in_receipt','Recibo de compra')], 'Tipo de Movimiento')

class SunatDocumentType(models.Model):
    _inherit = 'sunat.document.type'

    move_type = fields.Selection(selection=[
        ('entry','Asiento contable'),
        ('out_invoice','Comprobante de Pago'),
        ('out_refund','Nota de Crédito de cliente'),
        ('in_invoice','Factura de proveedor'),
        ('in_refund','Factura rectificativa de proveedor'),
        ('out_receipt','Recibo de ventas'),
        ('in_receipt','Recibo de compra')], string='Tipo de Movimiento', related="sunat_code.move_type")
    lower_range = fields.Integer(string='Rango inferior')
    top_range = fields.Integer(string='Rango superior')
    authorization_number = fields.Char(string='Nro. de Autorización')
