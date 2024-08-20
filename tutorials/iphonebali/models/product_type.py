from odoo import models, fields

class ProductType(models.Model):
    _name = 'product.type'
    _description = 'iphonebali product type'

    name = fields.Char('name', required=True)

    _sql_constraints = [
        ('unique_product_type_name', 'UNIQUE(name)', 'The product type name must be unique')
    ]