import json
from django.core.urlresolvers import reverse
from django.test import Client
from unittest import TestCase
from django.test.utils import override_settings


class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    @override_settings(GEOIP_PATH='/wrong/directory/')
    def test_wrong_geoip_path(self):
        """
        Check that settings an invalid path yields a HTTP 500.
        """
        url = reverse('easygeoip:geoip-explicit-ip-view', args=("95.12.13.14",))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 500)

    def test_invalid_ip_address(self):
        """
        Test that giving an invalid IP address yields a HTTP 400.
        """
        url = reverse('easygeoip:geoip-explicit-ip-view', args=("0.0.0.0",))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 400)

    def test_valid_ip_address(self):
        """
        Test that giving a valid IP address yields an object containing specific information.
        """
        example_dot_com_ip = "93.184.216.34"
        url = reverse('easygeoip:geoip-explicit-ip-view', args=(example_dot_com_ip,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(json.loads(res.content), {
            "city": "Norwell",
            "continent_code": "NA",
            "region": "MA",
            "charset": 0,
            "area_code": 781,
            "longitude": -70.82279968261719,
            "country_code3": "USA",
            "latitude": 42.15079879760742,
            "postal_code": "02061",
            "dma_code": 506,
            "country_code": "US",
            "country_name": "United States",
            "ip_address": "93.184.216.34"
        })



