# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from dateutil import relativedelta
from io import BytesIO
import datetime
import pytz
import xlsxwriter


class LessAttendanceReport(models.TransientModel):
    _name = 'controller.example.report'
    _description = 'Less Attendance Report'

    date_from = fields.Date(string='Date From', required=True,
                            default=datetime.datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
                          default=str(datetime.datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[
                                  :10])

    def print_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/controller_example_report/%s' % (self.id),
            'target': 'new',
        }

    def generate_xlsx_report(self):
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        worksheet = workbook.add_worksheet('Sheet 1')
        row = 2
        colm = 0
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        cell_format1 = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'border': 1})
        cell_format2 = workbook.add_format({'font_size': 12, 'align': 'center'})
        # num_cell_format = workbook.add_format({'font_size':12,'align':'center','num_format': '#,###'})
        cell_format1.set_bg_color('yellow')
        # header_bold_formate = workbook.add_format({'bold': True, 'font_size': 15})
        # from_month = self.date_from.strftime("%B")
        # to_month = self.date_to.strftime("%B")
        worksheet.write(2, 2, 'Employee Name', cell_format1)
        workbook.close()
        return fp.getvalue()
