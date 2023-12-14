# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, _, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate management'
    # _order = "sequence"

    name = fields.Char('Real Estate Name', default='Unknown', required=True, translate=True)
    description = fields.Text('Description of the asset', required=True)
    postcode = fields.Char('ZIP code')
    date_availability = fields.Date('Date availability', default=fields.Datetime.today()+timedelta(days=90), copy=False)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()   
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Orientation is used to specify the garden orientation')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be strictly positive.')
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink(self):
        for record in self:
            if record.state != 'new' and record.state != 'canceled':
                raise UserError(_('The property is not in state new or canceled, you cannot delete it.'))

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_('The property was canceled, you cannot sell.'))
            elif record.state == 'sold':
                raise UserError(_('The property is already in state sold.'))
            else:
                record.state = 'sold'
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('The property was sold, you cannot cancel.'))
            elif record.state == 'canceled':
                raise UserError(_('The property is already in state canceled.'))
            else:
                record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and not float_is_zero(record.selling_price, 2):
                min_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_price, 2) < 0:
                    raise ValidationError(_('Selling price must be at least 90% of the expected price.'))
