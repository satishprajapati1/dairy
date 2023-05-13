# -*- coding: utf-8 -*-
from odoo import http
# from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from odoo.http import request, serialize_exception, content_disposition
from odoo.tools import html_escape
import json

class DownloadXlsReports(http.Controller):

    @http.route('/web/collection_report/<model("collection.report"):model>', type='http', auth="user")
    def download_report_xls(self, model, **kw):
        # Method to download xls report without creating attachment
        data = model.generate_xlsx_report()
        filename = 'Collection Report'
        try:
            if not data:
                return request.not_found()
            else:
                return request.make_response(
            data,
            [('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', content_disposition(
            filename + '.xlsx'))])
        except Exception as e:
            se = serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}
            return request.make_response(html_escape(json.dumps(error)))
