from odoo import models, fields
from datetime import timedelta

class Product(models.Model):
    _name = 'product'
    _description = 'iphonebali product'

    def get_availability_date(self):
        return fields.Date.today() + timedelta(days=90)

    name = fields.Char(required=True)
    description = fields.Text()
    sku = fields.Char()
    date_availability = fields.Date(copy=False, default=get_availability_date)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    processor = fields.Char()
    memory = fields.Integer(default=4)
    storage = fields.Integer(default=128)
    battery_capacity = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'), 
        ('offer_received', 'Offer received'), 
        ('offer_accepted', 'Offer accepted'), 
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True)