from odoo import http
from odoo.http import request

class WebsiteSnippetPage(http.Controller):
    @http.route('/travel/booking', type='json', auth='public', website=True)
    def snippet_pages(self, **kw):
        booking = request.env['booking.booking'].sudo().search([],order="booking_date desc")
        values = [[
               bookings.booking_reference, bookings.id
            ]for bookings in booking]
        new = [values[i:i+4]for i in range(0, len(values), 4)]
        print(new,'000')
        return new

    @http.route('/travel/booking/new', type='http', auth='public', website=True, csrf=False)
    def snippet_page(self, **kw):
        booking_id = kw.get('booking_id')
        booking = request.env['booking.booking'].sudo().browse(int(booking_id))

        values = {
                'booking':  booking
            }

        return request.render('travel_management.travel_management_snippet_img', values)
