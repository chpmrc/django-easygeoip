import os
from django.conf import settings


# Provide necessary defaults

# GeoIP database directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_DATA_DIR = "easygeoip/geoip_data/"


def get_geoip_path():
    """
    We evaluate the path at runtime to be able to override settings in tests.
    """
    return getattr(settings, 'GEOIP_PATH', os.path.join(BASE_DIR, DEFAULT_DATA_DIR))