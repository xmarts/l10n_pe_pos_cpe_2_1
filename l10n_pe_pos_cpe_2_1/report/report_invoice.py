# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PosInvoiceReport(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_invoice'

    @api.model
    def render_html(self, docids, data=None):
        res = super(PosInvoiceReport, self).render_html(docids=docids, data=data)
        return res

