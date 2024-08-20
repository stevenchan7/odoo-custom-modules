from odoo import models, fields

class ProductTag(models.Model):
    _name = 'product.tag'
    _description = 'Product tags'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_product_tag_name', 'UNIQUE(name)', 'The product tag name must be unique')
    ]
    