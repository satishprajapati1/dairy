import base64

from odoo import fields, models, api,_
from odoo.tools import email_normalize

class Member(models.Model):
    _name = 'dairy.member'
    _inherit = [
        'mail.thread', 'mail.activity.mixin'
    ]
    _inherits = {'res.partner':'partner_id'}
    _description = 'Dairy Member'

    member_ref = fields.Char(string='Member Reference',tracking=True, required=True,readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
                                 string='Member Name')
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
    cattle_ids = fields.One2many('dairy.cattle', 'owner_id', string='Cattles')
    # collection
    collection_ids = fields.One2many('dairy.collection', 'member_id', string="Collection")
    total_collection = fields.Float(compute='_count_total_collection',default=0.0,help="Shows Current Year Collection")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        required=False)

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date().today()
                birthday = record.birth_date
                record.age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    @api.model
    def create(self, vals):
        if vals.get('member_ref', _('New')) == _('New'):
            vals['member_ref'] = self.env['ir.sequence'].next_by_code('dairy.member') or _('New')
        res = super(Member, self).create(vals)
        res.user_id = self.env['res.users'].with_context(no_reset_password=True)._create_user_from_template({
                'name': res.partner_id.name,
                'login': email_normalize(res.partner_id.email),
                'email': email_normalize(res.partner_id.email),
                'password': res.partner_id.phone,
                'partner_id': res.partner_id.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        })
        return res

    def action_view_collection(self):
        res = self.env.ref("dairy.dairy_collection_act_window").read()[0]
        res["domain"] = [("member_id", "=", self.id)]
        return res

    @api.depends('collection_ids')
    def _count_total_collection(self):
        for rec in self:
            rec.total_collection = sum(rec.env['dairy.collection'].search([('member_id','=',rec.id)]).mapped("amt"))
