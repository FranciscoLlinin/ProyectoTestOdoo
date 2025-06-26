# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class DeliveryDetailLine(models.Model):
    _name = 'delivery.detail.line'


    delivery_detail_id = fields.Many2one(
        'delivery.detail',
    )
    qty = fields.Float(
    )
    uom_id = fields.Many2one(
        'uom.uom',
    )
