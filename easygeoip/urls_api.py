from django.conf.urls import url

# API URLs
from .views import LocationFromIpView

urlpatterns = [
    url(r'^location/(?P<ip_address>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))/$', LocationFromIpView.as_view(),
        name='geoip-explicit-ip-view'),
    url(r'^location/$', LocationFromIpView.as_view(), name='geoip-implicit-ip-view')  # Take IP addr from request
]
