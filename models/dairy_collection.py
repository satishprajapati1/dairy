from odoo import fields, models, api


class Collection(models.Model):
    _name = 'dairy.collection'
    _description = 'Dairy Collection'

    name = fields.Many2one('dairy.member',string='Member Name')
    cattle_type = fields.Many2one('cattle.type')
    qty = fields.Float(string='Quality (Ltr.) ')
    fat = fields.Float()
    # fatperrate = fields.Many2one('fatrate',domain="[('type','=',cattle_type)]",string='Rate (per Fat)',required=True)
    # frate = fields.Float(related="fatperrate.rate",readonly=True)
    rate = fields.Float(string="Rate (per ltr)")
    # compute='_compute_rate',
    # compute='_compute_amt',
    amt = fields.Float()
