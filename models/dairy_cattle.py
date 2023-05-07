from odoo import fields, models, api,_


class Cattle(models.Model):
    _name = 'dairy.cattle'
    _inherit = [
        'mail.thread', 'mail.activity.mixin'
    ]
    _description = 'Dairy Cattle'

    image = fields.Binary(
        "Image")
    name = fields.Char(string='Cattle Reference',tracking=True, required=True,readonly=True, default=lambda self: _('New'))
    cattle_type_id = fields.Many2one('cattle.type')
    cattle_breed_id = fields.Many2one('cattle.breed', domain="[('cattle_type_id','=',cattle_type_id)]")
    height = fields.Float()
    weight = fields.Float()
    body_condition = fields.Selection([('fit', 'Fit'), ('sick', 'Sick'), ('weak', 'Weak')],default='fit')
    owner_id = fields.Many2one('dairy.member')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dairy.cattle') or _('New')
        return super(Cattle, self).create(vals)

class CattleType(models.Model):
    _name = 'cattle.type'
    _description = 'Cattle Type'
    _order = 'name'

    name = fields.Char(string='Name')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    # collection_ids = fields.One2many('dairy.collection','cattle_type_id')
    # collection_amount = fields.Float(compute='_count_collection_amount',default=0.0)

    _sql_constraints = [
        ('type_uniq','unique(name)','Cattle Type must be unique')
    ]

    # def action_view_collection_of_type(self):
    #     res = self.env.ref("dairy.dairy_collection_act_window").read()[0]
    #     res["domain"] = [("cattle_type_id", "=", self.id)]
    #     return res
    #
    # @api.depends('collection_ids')
    # def _count_collection_amount(self):
    #     for rec in self:
    #         rec.collection_amount = sum(rec.env['dairy.collection'].search([('cattle_type_id', '=', rec.id)]).mapped("amt"))


class CattleBreed(models.Model):
    _name = 'cattle.breed'
    _description = 'Cattle Breed'
    _order = 'name'

    name = fields.Char(string='Breed name')
    cattle_type_id = fields.Many2one('cattle.type',required=True,string='Cattle Type')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('breed_uniq','unique(name)','Cattle Breed must be unique')
    ]
