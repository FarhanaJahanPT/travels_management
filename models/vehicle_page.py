from odoo import models, fields


class VehicleCharges(models.Model):
    _name = 'charges'
    _description = 'vehicle charges'


    def default_unit(self):
        unit = self.env.ref('uom.product_uom_unit')
        print(unit)
        return unit.id

    service = fields.Selection([
        ('Maintanance', 'Maintanance'),
        ('Repair', 'Repair'),
        ('Petrol', 'Petrol'),
        ('others','others')],
        string='Service')
    quantity = fields.Integer(string= 'Quantity')
    unit = fields.Many2one('uom.uom',string= 'Unit',default=default_unit,store=True)
    amount = fields.Float(string= 'Amount')
    vehicle_id = fields.Many2one('vehicle.vehicle')



