from typing import io

import xlsxwriter

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from odoo.tools.safe_eval import json
import io


class Reporting(models.TransientModel):
    _name = 'travels.reporting'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one('res.partner', string='Customer')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')



    def travel_print_report(self):
        cr = self._cr
        query = """SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS SL_NO,location_location.address AS source_location,(
                    SELECT location_location.address AS destination_location
                       FROM location_location
                       WHERE location_location.id = tour_package.destination_location_id),vehicle_vehicle.vehicle_name,tour_package.state,res_partner.name,tour_package.start_date,tour_package.end_date,(
                    SELECT booking_booking.booking_reference
                        FROM booking_booking
                       WHERE booking_booking.id = tour_package.id)
                    FROM tour_package
                    INNER JOIN vehicle_vehicle
                    ON vehicle_vehicle.id = tour_package.vehicle_id
                    INNER JOIN location_location
                    ON location_location.id = tour_package.source_location_id
                    INNER JOIN res_partner
                    ON res_partner.id = tour_package.customer_id
                WHERE 1=1
                """
        if self.customer_id:
            query += """and tour_package.customer_id = %s""" % self.customer_id.id
        if self.date_from:
            query += """and tour_package.start_date >= '%s'  """ % self.date_from
        if self.date_to:
            query += """and tour_package.end_date <= '%s'""" % self.date_to
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValidationError("please enter valid dates")

        cr.execute(query)
        sql_dict = cr.dictfetchall()
        print(sql_dict)

        data = {

            'model_id': self.id,
            'to_date': self.date_to,
            'from_date': self.date_from,
            'partner_id': self.customer_id.name,
            'sql_dict': sql_dict
        }
        print(data)
        return self.env.ref('travel_management.action_report_travel').report_action(None, data=data)

    def travel_print_xlsx(self):
        cr = self._cr
        query =  """SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS SL_NO,location_location.address AS source_location,(
                    SELECT location_location.address AS destination_location
                       FROM location_location
                       WHERE location_location.id = tour_package.destination_location_id),vehicle_vehicle.vehicle_name,tour_package.state,res_partner.name,tour_package.start_date,tour_package.end_date,(
                    SELECT booking_booking.booking_reference
                        FROM booking_booking
                       WHERE booking_booking.id = tour_package.id)
                    FROM tour_package
                    INNER JOIN vehicle_vehicle
                    ON vehicle_vehicle.id = tour_package.vehicle_id
                    INNER JOIN location_location
                    ON location_location.id = tour_package.source_location_id
                    INNER JOIN res_partner
                    ON res_partner.id = tour_package.customer_id
                WHERE 1=1
                """
        if self.customer_id:
            query += """and tour_package.customer_id = %s""" % self.customer_id.id
        if self.date_from:
            query += """and tour_package.start_date >= '%s'  """ % self.date_from
        if self.date_to:
            query += """and tour_package.end_date <= '%s'""" % self.date_to
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValidationError("please enter valid dates")

        cr.execute(query)
        sql_dict = cr.dictfetchall()
        print(sql_dict)
        print('111111111111')
        print(query)
        data = {
            'model_id' : self.id,
            'customer_id':self.customer_id.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'sql_dict':sql_dict
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'travels.reporting',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Travel Management Report',
                     },
            'report_type' : 'xlsx'
        }

    def get_xlsx_report(self, data, response):


        print('000000000')
        print(response,'res')
        print(data,'data')
        value=[]
        model_id = data['model_id']
        customer_id = data['customer_id']
        from_date = data['date_from']
        to_date = data['date_to']
        sql_dict = data.get('sql_dict')
        user_obj = self.env.user
        output = io.BytesIO()
        print('1')
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        print('2')
        sheet = workbook.add_worksheet()
        print('3')
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        print('4')
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        print('5')
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        print('6')
        format = workbook.add_format({'font_size':'10px','border': 5,'align': 'center'})
        print('7')
        format5 = workbook.add_format({'font_size':'10px','border': 6,'align': 'center'})
        print('8')

        print('9')
        if customer_id or from_date or to_date :
            sheet.merge_range('G2:N3', 'Travels Management Report', head)
        else:
            sheet.merge_range('G8:N9', 'Travels Management Report', head)
        if customer_id:
            sheet.merge_range('F6:G6', 'Customer:', cell_format)
            sheet.merge_range('H6:I6', customer_id, cell_format)

        if from_date:
            sheet.merge_range('F8:G8', 'From Date:', cell_format)
            sheet.merge_range('H8:I8', from_date, cell_format)



        if to_date:
            sheet.merge_range('F10:G10', 'To Date:',cell_format)
            sheet.merge_range('H10:I10', to_date, cell_format)



        sheet.write('F13','SL_NO',format)
        print('10')
        sheet.merge_range('G13:H13', 'Booking Reference', format)
        sheet.merge_range('I13:J13', 'Source Location', format)
        sheet.merge_range('K13:L13', 'Destination Location', format)
        sheet.merge_range('M13:N13', 'Vehicle', format)
        sheet.merge_range('O13:P13', 'State', format)
        row=13
        for line in sql_dict:
            sheet.set_row(row, 20,txt)
            sheet.write(f'F{row+1}',line['sl_no'],format5)
            # sheet.write(row,7,line['booking_reference'])
            sheet.merge_range(f'G{row+1}:H{row+1}', line['booking_reference'],format5)
            sheet.merge_range(f'I{row+1}:J{row+1}',line['source_location'],format5)
            sheet.merge_range(f'K{row+1}:L{row+1}',line['destination_location'],format5)
            sheet.merge_range(f'M{row+1}:N{row+1}',line['vehicle_name'],format5)
            sheet.merge_range(f'O{row+1}:P{row+1}',line['state'],format5)
            row +=1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
