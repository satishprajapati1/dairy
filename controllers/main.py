# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from odoo.http import request


class DownloadXlsReports(http.Controller):

    @http.route('/web/controller_example_report/<model("controller.example.report"):model>', type='http', auth="user")
    @serialize_exception
    def download_report_xls(self, model, **kw):
        # Method to download xls report without creating attachment
        data = model.generate_xlsx_report()
        filename = 'Controller Example Report'
        if not data:
            return request.not_found()
        else:
            return request.make_response(
        data,
        [('Content-Type', 'application/octet-stream'),
        ('Content-Disposition', content_disposition(
        filename + '.xlsx'))])

