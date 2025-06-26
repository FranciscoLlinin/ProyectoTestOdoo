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

    def _get_delivery_summary_data(self):
        """
        Método para obtener los datos de resumen de entrega para reportes
        Agrupa por cantidad y unidad de medida
        """
        # Crear detalles si no existen
        if not self.delivery_detail_ids:
            self.env['delivery.detail'].create_delivery_details(self.id)
        
        delivery_details = self.delivery_detail_ids
        summary_data = []
        # Diccionario para agrupar por unidad de medida
        grouped_data = {}
        
        for detail in delivery_details:
            for line in detail.delivery_detail_line_ids:
                uom_name = line.uom_id.name or 'Sin UoM'
                
                if uom_name in grouped_data:
                    grouped_data[uom_name] += line.qty
                else:
                    grouped_data[uom_name] = line.qty
        
        # Convertir a lista para el template
        for uom_name, total_qty in grouped_data.items():
            summary_data.append({
                'qty': total_qty,
                'uom_name': uom_name,
            })
        
        return summary_data
    
    def _get_delivery_lots_data(self):
        """
        Método para obtener los datos de lotes y números de serie para reportes
        """
        # Crear detalles si no existen
        if not self.delivery_detail_ids:
            self.env['delivery.detail'].create_delivery_details(self.id)
        
        delivery_details = self.delivery_detail_ids
        lots_data = []
        
        for detail in delivery_details:
            for line in detail.delivery_detail_line_ids:
                if line.lot_serial_numbers:  # Solo agregar si tiene lotes/series
                    lots_data.append({
                        'product_name': line.product_name or 'Sin nombre',
                        'lot_serial_numbers': line.lot_serial_numbers,
                    })
        
        return lots_data
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