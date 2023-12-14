# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate tag (cozy, renovated)"
    # _order = "sequence"

    name = fields.Char('Real Estate Tag', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Property tags must be unique.'),
    ]
