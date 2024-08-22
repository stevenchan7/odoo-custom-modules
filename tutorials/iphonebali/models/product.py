from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import timedelta

class Product(models.Model):
    _name = 'product'
    _description = 'Iphonebali Product'
    _order = 'id desc'

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
    ], default='new', store=True, copy=False, compute="_compute_state")
    best_price = fields.Float(compute='_compute_best_price')
    refresh_rate = fields.Integer()
    camera_pixel = fields.Integer()

    # Relations
    product_type_id = fields.Many2one("product.type", string="Product type")
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    sales_person = fields.Many2one('res.users', string='Sales person', default=lambda self: self.env.user)
    product_tag_ids = fields.Many2many('iphonebali.product.tag', string='Product tags')
    product_offer_ids = fields.One2many('product.offer', 'product_id', string='Product offers')

    @api.depends('product_offer_ids.price')
    def _compute_best_price(self):
        for product in self:
            if product.product_offer_ids:
                product.best_price = max(product.product_offer_ids.mapped('price'))
            else:
                product.best_price = 0.0

    @api.depends('product_offer_ids')
    def _compute_state(self):
        for product in self:
            if len(product.product_offer_ids) > 0:
                product.state = 'offer_received'

    def sold_product(self):
        for product in self:
            if product.state == 'canceled':
                raise UserError(_('Canceled products cannot be sold'))
            else:
                product.state = 'sold'
                return True 

    def cancel_product(self):
        for product in self:
            if product.state == 'sold':
                raise UserError(_('Sold products cannot be canceled'))
            else:
                product.state = 'canceled'
                return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for product in self:
            # Selling price must not be zero for the constrains to be applied
            if not float_is_zero(product.selling_price, precision_rounding=0.01):
                min_selling_price = product.expected_price * 0.9
                # selling_price is lower than min_selling_price
                if float_compare(product.selling_price, min_selling_price, precision_rounding=0.01) == -1:
                    raise ValidationError(_('Selling price cannot be lower than 90 of expected price'))
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0.0)', 'Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0.0)', 'Selling price must be positive'),
    ]

