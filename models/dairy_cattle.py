from odoo import fields, models, api


class Cattle(models.Model):
    _name = 'dairy.cattle'
    _description = 'Dairy Cattle'

    image = fields.Binary(
        "Image")
    name = fields.Char()
    cattle_type = fields.Many2one('cattle.type')
    cattle_breed = fields.Many2one('cattle.breed', domain="[('type','=',cattle_type)]")
    height = fields.Float()
    weight = fields.Float()
    body_condition = fields.Selection([('fit', 'Fit'), ('sick', 'Sick'), ('weak', 'Weak')],default='fit')
    owner_id = fields.Many2one('dairy.member')


class CattleType(models.Model):
    _name = 'cattle.type'
    _description = 'Cattle Type'
    _order = 'name'

    name = fields.Char(string='Name')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('type_uniq','unique(name)','Cattle Type must be unique')
    ]


class CattleBreed(models.Model):
    _name = 'cattle.breed'
    _description = 'Cattle Breed'
    _order = 'name'

    name = fields.Char(string='Breed name')
    type = fields.Many2one('cattle.type',required=True,string='Cattle Type')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
