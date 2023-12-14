from datetime import timedelta
from odoo import api, fields, _, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    # _order = "sequence"

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", 
                                compute="_compute_date_deadline", 
                                inverse="_inverse_date_deadline_from")

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(price >= 0)', 'The offer price must be strictly positive.')
    ]

    #TODO please review :-)
    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if not property_id:
            raise UserError(_("Property not specified."))

        offers = self.search([('property_id', '=', property_id), ('status', '!=', 'refused')])

        if offers and any(offer.price > vals.get('price') for offer in offers):
            raise UserError(_("You cannot create an offer with a lower amount than an existing offer."))

        property = self.env['estate.property'].browse(property_id)
        if not property.exists():
            raise UserError(_("Property not found."))
        property.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date or fields.Datetime.today()
            if record.validity:
                if record.create_date:
                    record.date_deadline = date + timedelta(days=record.validity)
                else:
                    record.date_deadline = date + timedelta(days=record.validity)
            else:
                record.date_deadline = None

    def _inverse_date_deadline_from(self):
        for record in self:
            date = record.create_date or fields.Datetime.now()

        # If date_deadline is set, calculate validity
        if record.date_deadline:
            delta = record.date_deadline - date.date()
            record.validity = delta.days
        else:
            record.validity = 7  # Or set to a default value

    def action_accept(self):
        self.ensure_one()
        if self.property_id.partner_id:
            raise UserError(_("The buyer has already been set."))
        self.status = "accepted"
        self.env["estate.property"].browse(self.property_id.id).write(
            {
                "selling_price": self.price,
                "partner_id": self.partner_id.id,
                "state": "offer_accepted",
            }
        )
        return True

    def action_refuse(self):
        self.write({'status': 'refused'})