from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate property tag"
    _order = "name"
    _sql_constraints = [
        (
            "unique_tag_name",
            "UNIQUE(name)",
            "The property tag with same name already exists.",
        ),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
