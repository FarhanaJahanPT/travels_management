from odoo import models, fields, api


class EstimationAmount(models.Model):
    _name = 'estimation.amount'
    _description = 'estimation amounts'

    service = fields.Selection([
        ('Maintanance', 'Maintanance'),
        ('Repair', 'Repair'),
        ('Petrol', 'Petrol'),
        ('others', 'others')],
        string='Service')
    quantity = fields.Integer(string= 'Quantity')
    amount = fields.Float(string= 'Amount')
    subtotal = fields.Float(string='Sub Total',compute='_compute_subtotal',readonly=True)
    booking_id = fields.Many2one('booking.booking')
    # total_amount = fields.Float(string='Total Amount',readonly=True,compute='_compute_total_amount')

    @api.depends('quantity', 'amount')
    def _compute_subtotal(self):
       for record in self:
            record.subtotal = record.quantity * record.amount



