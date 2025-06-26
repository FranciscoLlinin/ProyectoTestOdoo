# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_show_delivery_details(self):
        """
        Acción para mostrar los detalles de entrega desde el botón inteligente
        """
        self.ensure_one()
        
        # Crear detalles de entrega si no existen
        if not self.delivery_detail_ids:
            self.env['delivery.detail'].create_delivery_details(self.id)
        
        # Configurar la acción para mostrar la vista
        action = {
            'name': _('Detalle de entrega'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'delivery.detail',
            'domain': [('account_move_id', '=', self.id)],
            'context': {
                'default_account_move_id': self.id,
                'create': False,
            },
            'target': 'current',
        }
        
        return action

    # ------------------------------------------------------
    # CRUD METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('delivery_detail_ids')
    def _compute_delivery_detail_count(self):
        """Calcular la cantidad de detalles de entrega"""
        for record in self:
            record.delivery_detail_count = len(record.delivery_detail_ids)

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

    delivery_detail_ids = fields.One2many(
        'delivery.detail',
        'account_move_id',
        string='Detalles de Entrega',
    )
    
    delivery_detail_count = fields.Integer(
        string='Cantidad de Detalles de Entrega',
        compute='_compute_delivery_detail_count',
    )