# coding: utf-8

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEstateProperty(TransactionCase):

    def setUp(self):

        super(TestEstateProperty, self).setUp()
        self.EstateProperty = self.env['estate.property']
        # Create a test property
        self.test_property = self.EstateProperty.create({
            'name': 'Test Property',
            'description': 'Test Description',
            'expected_price': 100000,
            'state': 'new',
        })

    # Test cancel action on a property with state 'new' 
    def test_action_set_cancel_new(self):

        self.test_property.action_set_cancel()
        self.assertEqual(self.test_property.state, 'canceled', 'Cancel action should set the state to canceled')

    # Test cancel action on a property with state 'sold' 
    def test_action_set_cancel_sold(self):

        self.test_property.write({'state': 'sold'})
        with self.assertRaises(UserError):
            self.test_property.action_set_cancel()
            