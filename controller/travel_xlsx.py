# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name, **kw):
        print('kkkkkkkkkkkkkkkkkk')
        # uid = request.session.uid
        report_obj = request.env[model].sudo()
        print('report_obj',report_obj)
        options = json.loads(options)
        try:
            print('ffffffffff')
            if output_format == 'xlsx':
                print('dddddd')
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', 'dummy token')
                print(response,'response')
                return response
        except Exception as e:
            print('sssssss')
            se = http.serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
        return request.make_response(html_escape(json.dumps(error)))
