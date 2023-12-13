# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PropertyTypeModel(models.Model):
    _name = "estate.aurel.property.type.model"
    _description = "Property Type Model"

    name = fields.Char('Type name', required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", default=lambda self: self.env.user)
    user_id = fields.Many2one("res.users", string="User", copy=False)



