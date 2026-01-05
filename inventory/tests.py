from django.test import TestCase
from inventory.models import SparePart, SparePartTrace
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient

class SparePartTraceTestCase(TestCase):

    def setUp(self):
        # Create Vendor group
        vendor_group, _ = Group.objects.get_or_create(name="Vendor")

        # Create vendor user
        self.vendor_user = User.objects.create_user(username='vendor', password='test123')
        self.vendor_user.groups.add(vendor_group)

        # Create non-vendor user
        self.regular_user = User.objects.create_user(username='customer', password='test123')

        # Create a spare part
        self.part = SparePart.objects.create(
            name='Brake Pad X200',
            description='Premium high-quality brake pad for sedans.',
            part_number='BPX200',
            stock=100,
            price=500.00,
            location='Rabat'
        )

        self.client = APIClient()

    def get_token_for_user(self, username, password):
        # Get JWT token by posting to your real token endpoint
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password
        }, format='json')
        return response.data['access']

    def test_trace_creation_by_vendor(self):
        # Get vendor JWT token
        token = self.get_token_for_user('vendor', 'test123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Vendor creates a trace
        response = self.client.post('/api/part-traces/', {
            "spare_part_id": self.part.id,
            "event_description": "Manufactured at Factory X"
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('current_hash', response.data)
        self.assertEqual(response.data['spare_part']['id'], self.part.id)

    def test_trace_creation_by_non_vendor(self):
        # Get customer JWT token
        token = self.get_token_for_user('customer', 'test123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Customer tries to create a trace
        response = self.client.post('/api/part-traces/', {
            "spare_part_id": self.part.id,
            "event_description": "Unauthorized Event"
        }, format='json')

        self.assertEqual(response.status_code, 403)

    def test_trace_list_view(self):
        # Create a trace directly in DB
        SparePartTrace.objects.create(spare_part=self.part, event_description="Manufactured")

        # Anonymous user can list
        response = self.client.get('/api/part-traces/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)


