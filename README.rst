=========
EasyGeoIP
=========

**Note:** yes, I do know this app has PEP8 violations, is tightly coupled to DRF, yadda yadda yadda...It's useful for some people (me, first off), it's not for others. Feel free to open PRs but this is mostly a repository for myself (also a nice way to see how publishing a package to pypi works).

EasyGeoIP is a Django app that enables IP address-based geo-location capabilities to your Django project based on a locally
stored database released by `MaxMind <http://dev.maxmind.com/geoip>`_.

Why EasyGeoIP?
--------------

Because it's a nice wrapper over the included django.contrib.gis.geoip and doesn't require all that setup.
You just need to do `pip install django-easygeoip`.

Why not use a web API?
----------------------

Because you have to register, get an API key, there might be a limitation on the number of queries, you might want to
use the service even when their server is not available, you might want to use different API keys on a staging and
production server (which probably means registering two accounts). There are many reasons why a local database is preferrable.

How do I use it?
----------------

First off install the package (preferably in your virtual environment):
::

    pip install django-easygeoip

Add it to the INSTALLED_APPS
::

    INSTALLED_APPS = (
        ...
        'easygeoip',
        ...
    )

Include its URLs (you can change the prefix `api` to whatever you want)
::

    url(r'^api/', include('easygeoip.urls_api', namespace="easygeoip")),

Once integrated into your project you will have two available endpoints:

- `/api/location/<<ip_address>>/`
- `/api/location/`

The first endpoint will use the IP address specified in the URL. The second endpoint will use the IP address within
the request object (yes, it understands the `X-Forwarded-For` header). The responses are in JSON.

Examples
--------

Example request::

    GET /api/location/93.184.216.34/

Example response::

    HTTP 200 OK
    {
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
    }

Example response with invalid IP address::

    HTTP 400 Bad request
    {
      "reason": "Invalid IP address",
      "ip_address": "0.0.0.0"
    }

Example response with invalid configuration::

    HTTP 500 Internal server error
    {
      "reason": "Could not instantiate a GeoIP object. Did you set the GEOIP_PATH variable and downloaded the files?",
      "ip_address": "93.184.216.34",
      "exception_message": "GeoIP path must be a valid file or directory."
    }

Installation notes
------------------

Other than the usual drill (add to INSTALLED_APPS, include the URLs in your url_patterns etc.) there is one more step
in order for this app to work. The package django.contrib.gis.geoip, used in this app, requires some binary files.
Specifically the GeoIP.dat and GeoLiteCity.dat databases are needed.

This app provides a utility function/Celery task that
updates the aforementioned files. Alternatively the GeoIP Update Program can be installed as a distribution package
on the system itself. I strongly suggest to simply run the task periodically (e.g. using Celery Beat or similar).
The files are updated "the first Tuesday of every month" (from the GeoIP docs).

I want to download the files manually
-------------------------------------

Simply import easygeoip and run the task.
::

    from easygeoip import tasks
    tasks.update_geoip_database()


I want to run the task periodically
-----------------------------------

An example of a monthly task for Celery beat:
::

    CELERYBEAT_SCHEDULE={
        'update_geoip_database': {
            'task': 'easygeoip.tasks.update_geoip_database',
            'schedule': timedelta(days=30),
        },
        [...]
    })


In the end settings.GEOIP_PATH should point to the directory where such files are regardless of the system used. This
directory will also be used by this app to store the files. If not set the app will use the default path `/easygeoip/geoip_data/`.

Logging
-------

You can just add another logger to your LOGGING setting. Here is an example:
::

    'easygeoip': {
        'handlers': ['myhandler'],
        'propagate': True,
        'level': 'DEBUG',
    },

Testing
-------

To run the test suite simply run `./manage.py test easygeoip` from your project directory.

Pypi
----

The package is available here: https://pypi.python.org/pypi/django-easygeoip
