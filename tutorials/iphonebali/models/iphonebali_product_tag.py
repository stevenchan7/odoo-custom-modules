from odoo import models, fields

class ProductTag(models.Model):
    _name = 'iphonebali.product.tag'
    _description = 'Iphonebali Product Tag'
    _oder = 'name'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_product_tag_name', 'UNIQUE(name)', 'The product tag name must be unique')
    ]
    