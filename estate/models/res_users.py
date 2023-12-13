from odoo import fields, models


class ResUsers(models.Model):

    # --- Private ---
    _inherit = "res.users"

    # --- Fields Declaration ---

    # Relational
    property_ids = fields.One2many(
        "estate.property", "user_id", string="Properties", domain=[("state", "in", ["new", "offer received"])]
    )