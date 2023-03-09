from odoo import models, fields, api, _
from datetime import date
from datetime import timedelta


class TravelManagement(models.Model):
    _name = 'booking.booking'
    _description = 'travel management properties'
    _rec_name = 'booking_reference'
    _inherit = 'mail.thread'

    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    number_of_passengers = fields.Integer(string='No of Passengers', default=1)
    booking_reference = fields.Char(string='Booking Reference', required=True, default=lambda self: _('New'),
                                    readonly=True)
    service_id = fields.Many2one('service.service', string='Service')
    image = fields.Binary(related='service_id.image')
    period = fields.Integer(string='Period', readonly=True)
    booking_date = fields.Datetime(string='Booking Date', default=date.today())
    source_location_id = fields.Many2one('location.location', string='Source Location')
    destination_location_id = fields.Many2one('location.location', string='Destination Location')
    expiration_date = fields.Datetime(string='Expiration Date', readonly=True, compute='_compute_service_id')
    estimation_amount_ids = fields.One2many('estimation.amount', 'booking_id')
    is_tour_package = fields.Boolean(string="Is Tour Package")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    charges = fields.Float(string='Charges')
    total_amount = fields.Monetary(string='Total Amount', readonly=True, compute='_compute_total_amount',currency_field='currency_id')

    travel_date = fields.Datetime(string='Travel Date')
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Done', 'Done'),
        ('Confirmed', 'Confirmed'),
        ('Expired', 'Expired')],
        string='State', default="Draft")

    @api.model
    def create(self, vals):
        vals['booking_reference'] = self.env['ir.sequence'].next_by_code(
            'booking.booking') or _('New')
        return super(TravelManagement, self).create(vals)

    @api.onchange('source_location_id')
    def onchange_source_location_id_field(self):
        return {'domain': {'destination_location_id': [('id', '!=', self.source_location_id.id)]}}

    @api.onchange('service_id')
    def _compute_service_id(self):
        # print(self)
        for rec in self:
            rec.expiration_date = False
            if rec.booking_date:
                rec.expiration_date = rec.booking_date + timedelta(days=int(rec.service_id.expiration_period))
                rec.expiration_date = rec.expiration_date.date()
                # print(rec.expiration_date,'exp')

            rec.is_tour_package = rec.service_id.is_tour_package

    def button_in_conform(self):
        print(self)
        if self.expiration_date:

            if self.expiration_date >= self.booking_date:
                self.write({
                    'state': "Done"
                })
        else:
            self.write({
                'state': "Expired"
            })

    @api.depends('estimation_amount_ids.subtotal')
    def _compute_total_amount(self):
        for i in self:
            i.total_amount = sum(i.mapped('estimation_amount_ids.subtotal'))

    #         print(i.total_amount)

    def expire_booking(self):
        bookings = self.env['booking.booking'].search([])
        for booking in bookings:
            if booking.expiration_date < date.today():
                booking.write({'state': 'Expired'})

    def button_create_invoice(self):
        print("b")
        self.write({
            'state': 'Done'
        })
        print('hiii')

        if self.service_id.is_tour_package:
            vals = []
            for rec in self.estimation_amount_ids:
                value = {
                    'name': rec.service,
                    'quantity': rec.quantity,
                    'price_unit': rec.amount
                }
                vals.append((0, 0, value))
            print(vals)
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_line_ids': vals
            })
            #
            # if self.service_id.is_tour_package:
            #             booking = self.env['estimation.amount'].search([('service','=',self.id)])
            #             list1 = []
            #             for record in booking.Maintanance:
            #                 vals = {
            #                     'item_id' : record.estimation_amount_ids.service,
            #                     'quantity' : record.quantity,
            #                     'subtotal' : record.subtotal
            #
            #                 }
            #                 vals=(0,0,vals)
            #                 list1.append(vals)
            #
            #             # for record in booking.Repair:
            #             #     vals = {
            #             #         'item_id' : record.estimation_amount_ids.service,
            #             #         'quantity' : record.quantity,
            #             #         'subtotal' : record.subtotal
            #             #
            #             #     }
            #             #     vals=(0,0,vals)
            #             #     list1.append(vals)
            #             #
            #             # for record in booking.Petrol:
            #             #     vals = {
            #             #         'item_id' : record.estimation_amount_ids.service,
            #             #         'quantity' : record.quantity,
            #             #         'subtotal' : record.subtotal
            #             #
            #             #     }
            #             #     vals=(0,0,vals)
            #             #     list1.append(vals)
            #             #
            #             # for record in booking.others:
            #             #     vals = {
            #             #         'item_id' : record.estimation_amount_ids.service,
            #             #         'quantity' : record.quantity,
            #             #         'subtotal' : record.subtotal
            #             #
            #             #     }
            #             #     vals=(0,0,vals)
            #             #     list1.append(vals)
            #
            #             invoice = self.env['account.move'].create({
            #                 'move_type': 'out_invoice',
            #                 'invoice_date':fields.Date.today(),
            #                 'partner_id': self.customer_id.id,
            #                 'confirm_invoice_id': self.id,
            #                 'payment_reference': self.travel_date,
            #                 'event_name_id':self.id,
            #                 'invoice_line_ids': list1
            #
            #
            #
            #             })
            # #
            #         if self.service_id.is_tour_package:
            #             invoice = self.env['account.move'].create({
            #                 'move_type': 'out_invoice',
            #                 'partner_id': self.customer_id.id,
            #                 'payment_reference': self.travel_date,
            #                 'invoice_line_ids': [(0, 0, {
            #                     'name': self.estimation_amount_ids.service,
            #                     'price_unit': self.estimation_amount_ids.subtotal,
            #                 })],
            #             })

            print('invoice', invoice)
        else:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'payment_reference': self.travel_date,
                'invoice_line_ids': [(0, 0, {
                    'name': f"{self.booking_reference} ({self.service_id.name})",
                    'price_unit': self.charges,
                })],
            })

        return {
            'name': 'account.move.form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("account.view_move_form").id,
            'res_id': invoice.id,
            'target': 'current'
        }


    # @api.onchange('service_id')
    # def onchange_service_id_field(self):
    #     self.write({'estimation_amount_ids': [(5, 0)]})
    #     for rec in self.package_id.estimation_ids:
    #         self.env['estimation.amount'].create({
    #             'service': rec.service,
    #             'quantity': rec.quantity,
    #             'amount': rec.amount,
    #             'booking_id': self.id,
    #         })
    #     print('self.estimation_amount_ids', self.estimation_amount_ids)

# vals = [(5,0,0),[(0, 0, {'p_id':p_value, '':,}), (0, 0, {'p_id':p_value, '':,})]]



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        print(self.read())
        for line in self.order_line:
            if line.price_unit > 100:
                print(line.read())

        product_ids = self.env['product.product'].search([])
        print(product_ids.filtered(lambda l: l.company_id.currency_id.name == 'INR'))
        for rec in product_ids:
            # if rec.list_price:
            print(rec.company_id.currency_id.name)
