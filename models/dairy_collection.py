from odoo import fields, models, api

class Collection(models.Model):
    _name = 'dairy.collection'
    _description = 'Dairy Collection'
    _rec_name = 'create_date'
    _order = 'create_date desc'

    member_id = fields.Many2one('dairy.member',string='Member Name')
    cattle_type_id = fields.Many2one('cattle.type')
    qty = fields.Float(string='Quality (Ltr.) ')
    fat = fields.Float()
    fat_rate = fields.Float(compute='_set_rate_per_fat',readonly=True)
    rate = fields.Float(compute='_compute_rate',string="Rate (per ltr)")
    amt = fields.Float(compute='_compute_amt',string="Amount")

    @api.depends("fat_rate")
    @api.onchange("fat")
    def _compute_rate(self):
        for record in self:
            self.rate = record.fat_rate * record.fat

    @api.onchange("fat_rate")
    @api.onchange("fat,qty")
    def _compute_amt(self):
        for record in self:
            record.amt = (((record.fat)* record.qty) * record.fat_rate)

    @api.onchange('cattle_type_id')
    def _set_rate_per_fat(self):
        for record in self:
            record.fat_rate = self.env['collection.rate'].search([('date','<=',fields.Date().today()),('cattle_type_id','=',record.cattle_type_id.id)],limit=1,order='date desc').rate

class FatRate(models.Model):
    _name = 'collection.rate'
    _description = 'Rate of Milk on the basis of fat and ltr'
    _rec_name = 'fat'
    _order = 'date'

    date = fields.Date(default=fields.Date().today())
    fat = fields.Float(string='Fat',default=1)
    rate = fields.Float(string='Rate')
    cattle_type_id = fields.Many2one('cattle.type',string='Cattle Type')