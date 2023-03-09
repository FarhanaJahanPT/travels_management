from odoo import models, fields, api


class Estimation(models.Model):
    _name = 'estimation.estimation'
    _description = 'estimations'

    estimated_km = fields.Float(string= 'Estimated KM')

    service = fields.Selection([
        ('Maintanance', 'Maintanance'),
        ('Repair', 'Repair'),
        ('Petrol', 'Petrol'),
        ('others', 'others')],
        string='Service',readonly=True,store=True)
    quantity = fields.Integer(string= 'Quantity',readonly=True,store=True)
    amount = fields.Float(string= 'Amount',readonly=True,store=True)
    subtotal = fields.Float(string='Sub Total',compute='_compute_subtotal',readonly=True,store=True)
    tour_id = fields.Many2one('tour.package')
    # total_amount = fields.Float(string='Total Amount',readonly=True,compute='_compute_total_amount')

    @api.depends('quantity', 'amount')
    def _compute_subtotal(self):
       for record in self:
            record.subtotal = record.quantity * record.amount





