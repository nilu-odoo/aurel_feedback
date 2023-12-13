# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PropertyOfferModel(models.Model):
    _name = "estate.aurel.property.offer.model"
    _description = "Property Offer Model"

    name = fields.Char('Offer name', required=True)
    price = fields.Float('Price')
    status = fields.Selection(
        string = 'Status',
        copy = False,
        selection = [('A', 'Accepted'), ('R', 'Refused')])
    partner_id = fields.Many2one("estate.aurel.property.type.model", required=True, string="Partner")
    property_id = fields.Many2one("estate.aurel.test.model", required=True)



