from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsitePage(http.Controller):
    @http.route('/booking', type='http', auth='public', website=True)
    def web_page(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([])
        service_id = request.env['service.service'].sudo().search([])
        location_id = request.env['location.location'].sudo().search([])
        print(service_id,'llllll')
        return request.render('travel_management.website_page_booking', {'customer_id':customer_id,
                                                                         'service_id':service_id,
                                                                         'source_location_id':location_id,
                                                                         'destination_location_id':location_id})


class WebsitePageThanks(http.Controller):
    @http.route('/booking/submit/', type='http', auth='public', website=True)
    def create_web_page(self, **kw):
        print('kkk')


        print(kw.get('source_location_id'),kw.get('destination_location_id.id'),kw.get('number_of_passengers'),kw.get('service_id'))
        vals = request.env['booking.booking'].sudo().create({
            'customer_id': kw.get('customer_id'),
            'travel_date': kw.get('travel_date'),
            'source_location_id': kw.get('source_location_id'),
            'destination_location_id': kw.get('destination_location_id.id'),
            'number_of_passengers': kw.get('number_of_passengers'),
            'service_id': kw.get('service_id')
        })
        print(vals)
        value = {
            'vals': vals,
        }
        return request.render('travel_management.website_booking_thanks_menu', value)


class TravelsBookingMyPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        count = request.env['booking.booking'].search_count([('customer_id', '=', partner.id)])
        if 'travel_count' in counters:
            values['travel_count'] = count
        return values

    # @http.route(['/my/quotes', '/my/quotes/page/<int:page>'], type='http', auth="user", website=True)
    # def portal_my_quotes(self, **kwargs):
    #     values = self._prepare_sale_portal_rendering_values(quotation_page=True, **kwargs)
    #     request.session['my_quotations_history'] = values['quotations'].ids[:100]
    #     return request.render("sale.portal_my_quotations", values)

    @http.route('/my/travels', type='http', auth='user', website=True)
    def create_home_page(self, **kw):
        partners = request.env.user.partner_id
        bookings = request.env['booking.booking'].sudo().search([('customer_id', '=', partners.id)])
        # values = self._prepare_sale_portal_rendering_values(quotation_page=True, **kwargs)
        # request.session['my_quotations_history'] = values['quotations'].ids[:100]
        vals = {}
        vals.update({
            'partners': partners,
            'booking': bookings



        })
        return request.render('travel_management.portal_my_home_travels_booking', vals)



    @http.route('/new/account',type='http',auth='user',website=True)
    def web_account_page(self, **kw):
        print('hhh')
        return request.render('travel_management.website_create_account_menu', {})

    @http.route('/new/account/submit', type='http', auth='public', website=True)
    def create_new_account(self, **kw):
            customer = request.env['res.partner'].sudo().create({
                'name': kw.get('customer_id'),
                'phone': kw.get('phone'),
                'email' : kw.get('email')
            })
            print(customer)
            values = {
                'customer':customer.id,
            }
            # vals = request.env['booking.booking'].sudo().create({
            #     'customer_id': customer.id,
            #     'travel_date': kw.get('travel_date'),
            #     'source_location_id': kw.get('source_location_id'),
            #     'destination_location_id': kw.get('destination_location_id.id'),
            #     'number_of_passengers': kw.get('number_of_passengers'),
            #     'service_id': kw.get('service_id')
            # })
            # print(vals)
            # value = {
            #     'vals': vals,
            # }
            return request.redirect('/booking')



