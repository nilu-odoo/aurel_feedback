# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class TestModel(models.Model):
    _name = "estate.aurel.test.model"
    _description = "Test Model"

    property_type_id = fields.Many2one("estate.aurel.property.type.model", string="Property Type")
    user_id = fields.Many2one(related='property_type_id.user_id')
    partner_id = fields.Many2one(related='property_type_id.partner_id')

    tag_ids = fields.Many2many("estate.aurel.property.tag.model", string="Tags")

    offer_ids = fields.One2many("estate.aurel.property.offer.model", "property_id")

    active = fields.Boolean('Active', default=True)

    end_date  = fields.Date.today() + relativedelta(months=3)

    name = fields.Char('Plan name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post code')
    date_avaibility = fields.Datetime('Date', readonly=True, copy=False, default=end_date)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', required=True, default="2")
    living_area = fields.Integer('Living area', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage', readonly=False)
    garden = fields.Boolean('Garden', readonly=False)

    garden_area = fields.Integer('Garden Area', readonly=False)
    garden_orientation = fields.Selection(
        string = 'North',
        selection = [('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'Weast')],
        help = "Type is used to separate Leads and Opportunities")
        
    state = fields.Selection(
        string = 'State',
        copy = False,
        required = True,
        default = "New",
        selection = [('New', 'New'), ('Offer', 'Offer'), ('Received', 'Received'), ('Offer', 'Offer'), ('Accepted', 'Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')])


    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    validity = fields.Integer(compute="_compute_validity_date", inverse="_compute_deadline", default = "7")
    date_deadline = fields.Date("Deadline")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(self.offer_ids.mapped("price"), default=0)

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _compute_deadline(self):
        for record in self:
            record.date_deadline = self.create_date + relativedelta(days=self.validity)
        
        