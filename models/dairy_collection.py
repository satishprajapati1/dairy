from odoo import fields, models, api

class Collection(models.Model):
    _name = 'dairy.collection'
    _description = 'Dairy Collection'
    _inherit = [
        'mail.thread', 'mail.activity.mixin'
    ]
    _rec_name = 'collection_date'
    _order = 'collection_date desc'

    collection_date = fields.Datetime(string="Collection Date")
    member_id = fields.Many2one('dairy.member',string='Member Name',required=True)
    cattle_type_id = fields.Many2one('cattle.type',required=True)
    qty = fields.Float(string='Quantity (Ltr.) ',required=True)
    fat = fields.Float(required=True)
    fat_rate = fields.Float(compute='_set_rate_per_fat',readonly=True,store=True)
    rate = fields.Float(compute='_compute_rate',string="Rate (per ltr)",store=True)
    amt = fields.Float(compute='_compute_amt',string="Amount",store=True)


    @api.depends("fat_rate","fat")
    def _compute_rate(self):
        for record in self:
            record.rate = (record.fat_rate * record.fat)

    @api.depends("rate","qty")
    def _compute_amt(self):
        for record in self:
            record.amt = (record.qty * record.rate)

    @api.onchange('cattle_type_id')
    @api.depends('cattle_type_id')
    def _set_rate_per_fat(self):
        for record in self:
            record.fat_rate = record.env['collection.rate'].search([('date', '<=', fields.Date().today()), ('cattle_type_id', '=', record.cattle_type_id.id)], limit=1, order='date desc').rate


class FatRate(models.Model):
    _name = 'collection.rate'
    _description = 'Rate of Milk on the basis of fat and ltr'
    _rec_name = 'fat'
    _order = 'date'

    date = fields.Date(default=fields.Date().today())
    fat = fields.Float(string='Fat',default=1)
    rate = fields.Float(string='Rate')
    cattle_type_id = fields.Many2one('cattle.type',string='Cattle Type')
