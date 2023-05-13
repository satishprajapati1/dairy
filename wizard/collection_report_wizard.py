# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from dateutil import relativedelta
from io import BytesIO
import datetime
import pytz
import xlsxwriter


class CollectionReport(models.TransientModel):
    _name = 'collection.report'
    _description = 'Collection Report'

    date_from = fields.Date(string='Date From', required=True,
                            default=datetime.datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
                          default=str(datetime.datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[
                                  :10])

    def print_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/collection_report/%s' % (self.id),
            'target': 'new',
        }

    def generate_xlsx_report(self):
        collections = self.env['dairy.collection'].search([('collection_date','>=',self.date_from),('collection_date','<=',self.date_to)])
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        sheet = workbook.add_worksheet("Report")
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 16)
        sheet.set_column('E:E', 13)
        sheet.set_column('F:F', 13)
        bold = workbook.add_format({'bold': True, 'bg_color': 'yellow', 'border': 1, 'align': 'center'})
        name = workbook.add_format({'align': 'center'})
        date = workbook.add_format({'num_format': 'yyyy/mm/dd hh:mm', 'align': 'center'})
        format_float = workbook.add_format({'num_format': '#,##,##0.00', 'align': 'center'})
        column = 0
        row = 0
        sheet.write(row, column, "Date", bold)
        column += 1
        sheet.write(row, column, "Type", bold)
        column += 1
        sheet.write(row, column, "Quantity (Ltr)", bold)
        column += 1
        sheet.write(row, column, "Fat", bold)
        column += 1
        sheet.write(row, column, "Rate per Ltr", bold)
        column += 1
        sheet.write(row, column, "Amount", bold)
        row += 1
        for obj in collections:
            column = 0
            sheet.write(row, column, obj.create_date, date)
            column += 1
            sheet.write(row, column, obj.cattle_type_id.name, format_float)
            column += 1
            sheet.write(row, column, obj.qty, format_float)
            column += 1
            sheet.write(row, column, obj.fat, format_float)
            column += 1
            sheet.write(row, column, obj.rate, format_float)
            column += 1
            sheet.write(row, column, obj.amt, format_float)
            row += 1
        column -= 1
        sheet.write(row, column, "Total Amount", bold)
        column += 1
        sheet.write(row, column, sum(collections.mapped('amt')), format_float)
        # Add total quantity
        workbook.close()
        return fp.getvalue()
