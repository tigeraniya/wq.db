from rest_framework.test import APITestCase
from rest_framework import status
import json
from .models import RootModel, OneToOneModel


class UrlsTestCase(APITestCase):
    def setUp(self):
        instance = RootModel.objects.find('instance')
        instance.description = "Test"
        instance.save()
        OneToOneModel.objects.create(
            root=instance,
        )

    # Test existence and content of config.json
    def test_config_json(self):
        response = self.client.get('/config.json')
        result = json.loads(response.content)
        self.assertIn("pages", result)

    # Test url="" use case
    def test_list_at_root(self):
        response = self.client.get("/.json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data['list']) == 1)

    def test_detail_at_root(self):
        response = self.client.get('/instance.json')
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(response.data['description'] == "Test")

    # Ensure nested serializers are created for SerializableGenericRelations
    # (e.g. identifiers), but only for detail views
    def test_detail_nested_identifiers(self):
        response = self.client.get('/instance.json')
        self.assertIn('identifiers', response.data)
        self.assertEqual(response.data['identifiers'][0]['slug'], 'instance')

    def test_list_nested_identifiers(self):
        response = self.client.get('/.json')
        self.assertNotIn('identifiers', response.data['list'][0])