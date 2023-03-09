from odoo import models, fields, api


class Location(models.Model):
    _name = 'location.location'
    _description = 'locations'
    _rec_name = 'address'

    address = fields.Char(string='Address')



class Service(models.Model):
    _name = 'service.service'
    _description = 'service type'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    expiration_period = fields.Integer(string='Expiration period')
    is_tour_package = fields.Boolean(string="Is Tour Package")
    image = fields.Binary(string="Image")



class Facilities(models.Model):
    _name = 'facilities'
    _description = 'facilities'

    name = fields.Char(string='Facilities')



class Vehicle(models.Model):
    _name = 'vehicle.vehicle'
    _description = 'vehicles'
    _rec_name = 'vehicle_name'

    vehicle_name = fields.Char(string='Name', store=True, readonly=True)
    registration_no = fields.Char(string='Registration NO', required=True, index=True)
    _sql_constraints = [
        ('registration_no_unique', 'UNIQUE(registration_no)', "Registration no must be unique")]
    vehicle_type = fields.Selection([
        ('Bus', 'Bus'),
        ('Traveller', 'Traveller'),
        ('Van', 'Van'),
        ('Other', 'Other')],
        string='Vehicle Type')
    number_of_seat = fields.Integer(string='Number of Seats', default=1)
    facilities_ids = fields.Many2many('facilities', string='Facilities')
    vehicle_charges_ids = fields.One2many('charges', 'vehicle_id', string=" ")
    start_date = fields.Date(string='Date', invisible=True)



    @api.onchange('vehicle_type')
    def _onchange_vehicle_type(self):
        if self.registration_no:
            result_name = f"{self.registration_no} ({self.vehicle_type})"
            self.vehicle_name = result_name

