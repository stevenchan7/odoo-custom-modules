from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta

class ProductOffer(models.Model):
    _name = 'product.offer'
    _description = 'Product offer'

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ['refused', 'Refused']
    ], required=True, copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    product_id = fields.Many2one('product', required=True)
    validity = fields.Integer(required=True, default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.validity:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days
    
    def accept_offer(self):
        for offer in self:
            if offer.product_id.product_offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != offer.id):
                raise UserError(_('Only one offer can be accepted'))
            else:
                offer.status = 'accepted'
                offer.product_id.buyer = offer.partner_id
                offer.product_id.selling_price = offer.price
                offer.product_id._check_selling_price()
    
    def refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            offer.product_id.selling_price = 0.0
            offer.product_id.buyer = False

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0.0)', 'Offer price must be strictly positive')
    ]
