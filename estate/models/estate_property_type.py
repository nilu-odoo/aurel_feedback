# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate type (house, apartment, penthouse, castle…)"
    # _order = "sequence"

    name = fields.Char('Real Estate Type', required=True)

    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Property types must be unique.'),
    ]
