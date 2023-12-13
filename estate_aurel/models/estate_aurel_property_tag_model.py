# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PropertyTagModel(models.Model):
    _name = "estate.aurel.property.tag.model"
    _description = "Property Tag Model"

    name = fields.Char('Tag name', required=True)



