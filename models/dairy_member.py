from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
import re

class Member(models.Model):
    _name = 'dairy.member'
    _inherits = {'res.partner':'partner_id'}
    _description = 'Dairy Member'

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
                                 string='Related Partner', help='Partner-related data of the Member')
    active = fields.Boolean(default=True)
    birth_date = fields.Date(string="Birth Date")
    age = fields.Integer(compute="_compute_age",default=0)
    gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')])
    # Account Details
    bank_name = fields.Char()
    account_no = fields.Char()
    account_type = fields.Selection([('current', 'Current'), ('savings', 'Savings')])
    ifsc_code = fields.Char()
    branch = fields.Char(string='Branch name')
    # Cattles
    # cattles = fields.One2many('cattle', 'owner_name', string='Cattles')
    # collection
    # collections = fields.One2many('collection', 'name', string="Collection")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date().today()
                birthday = record.birth_date
                record.age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    # @api.constrains("phone")
    # def _check_phone(self):
    #     for rec in self:
    #         if rec.phone and len(rec.phone) != 10 and not str(rec.phone).isdigit():
    #             raise ValidationError(_("Phone number must be 10 valid digits"))
    #     return True