from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TourPackage(models.Model):
    _name = 'tour.package'
    _description = 'tour packages'
    _rec_name = 'customer_id'
    # _inherit = 'ir.rule'

    def default_tour_package(self):
        tour_package = self.env.ref('travel_management.service_data_properties')
        print(tour_package)
        return tour_package.id

    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    source_location_id = fields.Many2one('location.location', string='Source Location')
    destination_location_id = fields.Many2one('location.location', string='Destination Location')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    no_of_travellers = fields.Integer(string='Number of Travellers')
    facilities_ids = fields.Many2many('facilities', string='Facilities')
    estimation_ids = fields.One2many('estimation.estimation', 'tour_id')
    estimated_km = fields.Float(string='Estimated KM')
    vehicle_id = fields.Many2one('vehicle.vehicle')
    sale_order = fields.Many2one('sale.order')
    company_id = fields.Many2one('res.company',string='Company',required=True, index=True)
    total_amount = fields.Float(string='Total Amount', readonly=True, compute='_compute_total_amount')
    vehicle_type = fields.Selection([
        ('Bus', 'Bus'),
        ('Traveller', 'Traveller'),
        ('Van', 'Van'),
        ('Other', 'Other')],
        string='Vehicle Type')
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed')],
        string='State', default="Draft")
    name_id = fields.Many2one('service.service', default=default_tour_package)
    is_tour_package = fields.Boolean(related='name_id.is_tour_package')
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('estimation_ids.subtotal')
    def _compute_total_amount(self):
        for i in self:
            i.total_amount = sum(i.mapped('estimation_ids.subtotal'))
            print(i.total_amount)

    @api.onchange('source_location_id')
    def onchange_source_location_field(self):
        return {'domain': {'destination_location_id': [('id', '!=', self.source_location_id.id)]}}

    @api.onchange('vehicle_id')
    def onchange_vehicle_id_field(self):
        self.write({'estimation_ids': [(5, 0)]})
        for rec in self.vehicle_id.vehicle_charges_ids:
            self.env['estimation.estimation'].create({
                'service': rec.service,
                'quantity': rec.quantity,
                'amount': rec.amount,
                'tour_id': self.id,
            })
        print('self.estimation_ids', self.estimation_ids)

    def button_in_conform(self):
        self.write({
            'state': "Confirmed"
        })

    @api.constrains('vehicle_id')
    def check_vehicle_availability(self):
        print(self.vehicle_id, self.start_date, self.end_date, self.id)
        domain = [
            ('vehicle_id', '=', self.vehicle_id.id),
            ('start_date', '<=', self.end_date),
            ('end_date', '>=', self.start_date),
            ('id', '!=', self.id)
        ]

        reservations = self.search(domain)
        print('reservations', reservations)
        if reservations:
            raise ValidationError("The vehicle is not available between these dates.")

    @api.onchange('vehicle_type', 'no_of_travellers', 'facilities_ids')
    def onchange_vehicle_id(self):
        domain = []
        if self.vehicle_type:
            domain.append(('vehicle_type', '=', self.vehicle_type))
        if self.no_of_travellers:
            domain.append(('number_of_seat', '>=', self.no_of_travellers))
        if self.facilities_ids:
            domain.append(('facilities_ids', '=', self.facilities_ids.ids))
        return {
            'domain': {'vehicle_id': domain}
        }

    # @api.onchange('service_id')
    # def onchange_service_id(self):
    #
    #
    #     self.is_tour_package = self.is_tour_package

    def btn_in_conform(self):
        self.write({
            'state': "Confirmed"
        })
        booking_id = self.env['booking.booking'].create({

            'customer_id': self.customer_id.id,
            'travel_date': self.start_date,
            'source_location_id': self.source_location_id.id,
            'destination_location_id': self.destination_location_id.id,
            'number_of_passengers': self.no_of_travellers,
            'booking_date': fields.Date.today(),
            'service_id': self.name_id.id,
            'is_tour_package': self.is_tour_package
        })
        if self.is_tour_package:
            for rec in self.estimation_ids:
                self.env['estimation.amount'].create({
                    'service': rec.service,
                    'quantity': rec.quantity,
                    'amount': rec.amount,
                    'booking_id': booking_id.id
                })

        print('bokkingggg', booking_id)

        self.env['travels.reporting'].create({

            'customer_id': self.customer_id.id,
            'date_from': self.start_date,
            'date_to': self.end_date })

    # @api.model
    # def _compute_domain(self, record):
    #     domain = super()._compute_domain(record)
    #     if self.env.user.has_group('travel_management.group_travel_manager'):
    #         return domain
    #     else:
    #         return ['&', ('company_id', '=', self.env.user.company_id.id)] + domain
