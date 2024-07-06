from odoo import models, fields

class Product(models.Model):
    _name = 'product'
    _description = 'iphonebali product'

    name = fields.Char(required=True)
    description = fields.Text()
    sku = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(required=True, readonly=True, copy=False)
    processor = fields.Char()
    memory = fields.Integer()
    storage = fields.Integer()
    battery_capacity = fields.Integer()