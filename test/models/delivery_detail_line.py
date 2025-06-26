# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class DeliveryDetailLine(models.Model):
    _name = 'delivery.detail.line'
    _description = 'Línea de Detalle de Entrega'

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CONSTRAINTS AND VALIDATIONS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # OTHER METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------

    delivery_detail_id = fields.Many2one(
        'delivery.detail',
        string='Detalle de Entrega',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        readonly=True,
    )
    qty = fields.Float(
        string='Cantidad',
        readonly=True,
        digits='Product Unit of Measure',
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Medida',
        readonly=True,
    )