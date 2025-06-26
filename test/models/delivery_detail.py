# Part of Odoo and Trescloud. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class DeliveryDetail(models.Model):
    _name = 'delivery.detail'
    _description = 'Detalle de Entrega'
    _rec_name = 'picking_id'

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD METHODS
    # ------------------------------------------------------

    @api.model
    def create_delivery_details(self, invoice_id):
        """
        Método para crear los detalles de entrega basados en las transferencias
        relacionadas a una factura
        """
        invoice = self.env['account.move'].browse(invoice_id)
        if not invoice.exists():
            return False
            
        # Buscar las transferencias relacionadas con la factura
        # que estén en estado 'done'
        sale_order = False
        if invoice.invoice_origin:
            sale_order = self.env['sale.order'].search([('name', '=', invoice.invoice_origin)], limit=1)
        
        if not sale_order:
            return []
            
        pickings = self.env['stock.picking'].search([
            ('sale_id', '=', sale_order.id),
            ('state', '=', 'done'),
            ('picking_type_code', '=', 'outgoing'),
        ])
        
        delivery_details = []
        for picking in pickings:
            # Verificar si ya existe un detalle para esta transferencia y factura
            existing_detail = self.search([
                ('account_move_id', '=', invoice_id),
                ('picking_id', '=', picking.id)
            ], limit=1)
            
            if not existing_detail:
                # Crear el detalle de entrega
                detail_vals = {
                    'account_move_id': invoice_id,
                    'picking_id': picking.id,
                    'invoiced': False,
                }
                detail = self.create(detail_vals)
                # Crear las líneas de detalle
                self._create_detail_lines(detail, picking)
                delivery_details.append(detail)
        
        return delivery_details

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

    def _create_detail_lines(self, detail, picking):
        """
        Crear las líneas de detalle basadas en los movimientos de stock
        """
        DeliveryDetailLine = self.env['delivery.detail.line']
        
        # Agrupar movimientos por producto y unidad de medida
        grouped_moves = {}
        for move in picking.move_ids.filtered(lambda m: m.state == 'done'):
            key = (move.product_id.id, move.product_uom.id)
            if key not in grouped_moves:
                grouped_moves[key] = {
                    'qty': 0,
                    'product_id': move.product_id,
                    'uom_id': move.product_uom,
                }
            grouped_moves[key]['qty'] += move.quantity_done
        
        # Crear líneas de detalle
        for group_data in grouped_moves.values():
            if group_data['qty'] > 0:
                DeliveryDetailLine.create({
                    'delivery_detail_id': detail.id,
                    'product_id': group_data['product_id'].id,
                    'qty': group_data['qty'],
                    'uom_id': group_data['uom_id'].id,
                })

    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------

    account_move_id = fields.Many2one(
        'account.move',
        string='Factura',
        required=True,
        readonly=True,
    )
    picking_id = fields.Many2one(
        'stock.picking',
        string='Transferencia',
        required=True,
        readonly=True,
    )
    invoiced = fields.Boolean(
        string='Facturado',
        default=False,
        help='Indica si este detalle de entrega ha sido facturado',
        tracking=True,
    )
    delivery_detail_line_ids = fields.One2many(
        'delivery.detail.line',
        'delivery_detail_id',
        string='Líneas de Detalle',
        readonly=True,
    )
    picking_name = fields.Char(
        related='picking_id.name',
        string='Número de Transferencia',
        readonly=True,
    )
    picking_state = fields.Selection(
        related='picking_id.state',
        string='Estado de Transferencia',
        readonly=True,
    )