import json
import logging
from django.contrib.gis.geoip import GeoIP, GeoIPException
from django.http import HttpResponse
from django.views.generic import View
from easygeoip.settings import get_geoip_path

ERRORS = {
    'no_geoip_path': {
        'reason': 'Could not instantiate a GeoIP object. Did you set the GEOIP_PATH variable and downloaded the files?'
    },
    'invalid_ip_address': {
        'reason': 'Invalid IP address'
    }
}


logger = logging.getLogger(__name__)


class LocationFromIpView(View):
    """
    A simple endpoint that allows to retrieve geo-location information for a specific IP address.
    """
    def get(self, *args, **kwargs):
        ip_address = kwargs.get('ip_address')
        # If the app is running behind a proxy we have to check for the X-Forwarded-For header
        if not ip_address:
            ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR', '') or self.request.META.get('REMOTE_ADDR')
        try:
            logger.debug("Using path " + get_geoip_path())
            g = GeoIP(get_geoip_path())
        except GeoIPException as ge:
            return HttpResponse(json.dumps({
                'ip_address': ip_address,
                'reason': ERRORS['no_geoip_path']['reason'],
                'exception_message': ge.message
            }), status=500, content_type='application/json')
        location_info = g.city(ip_address)
        if not location_info:
            return HttpResponse(json.dumps({
                'ip_address': ip_address,
                'reason': ERRORS['invalid_ip_address']['reason']
            }), status=400, content_type='application/json')
        location_info['ip_address'] = ip_address
        return HttpResponse(json.dumps(location_info), content_type='application/json')
