import os
import requests
import logging
import gzip
from celery.task import task
from . import settings


GEOIP_BASE_URL = 'http://geolite.maxmind.com/download/geoip/database/'
GEOLITE_CITY_FILENAME = 'GeoLiteCity.dat.gz'
GEOIP_DIR = 'GeoLiteCountry/'
GEOIP_FILENAME = 'GeoIP.dat.gz'


logger = logging.getLogger(__name__)


def extract_gzip(filename):
    """
    Exctract the given gzip infile and write the content into outfile.
    """
    logger.info("Extracting " + filename)
    to_extract = gzip.open(filename, 'rb')
    extracted_filename = os.path.splitext(filename)[0]  # Remove .gz extension
    logger.info("Writing to " + extracted_filename)
    output = open(extracted_filename, 'wb')
    for line in to_extract:
        output.write(line)
    output.close()
    to_extract.close()


def download_file(url, outfile):
    """
    Download the given URL to the specified out_file.
    """
    logger.info("Downloading " + url)
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        output = open(outfile, 'wb')
        chunks = res.iter_content(chunk_size=1024)
        for chunk in chunks:
            if chunk:  # Filter out keep-alive chunks
                output.write(chunk)
        output.close()
        logger.info("Downloaded in " + outfile)
        return True
    else:
        logger.error("Resource " + url + " is not available (status code was " + str(res.status_code))
        return False


@task
def update_geoip_database():
    """
    Download and extract the database files needed for the django.contrib.gis.geoip package to work.
    """
    db_path = settings.get_geoip_path()
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    to_download = [
        {
            'outfile': db_path + GEOLITE_CITY_FILENAME,
            'url': GEOIP_BASE_URL + GEOLITE_CITY_FILENAME,
        },
        {
            'outfile': db_path + GEOIP_FILENAME,
            'url': GEOIP_BASE_URL + GEOIP_DIR + GEOIP_FILENAME
        }

    ]
    # Download and extract binary files
    for dbfile in to_download:
        if download_file(dbfile['url'], dbfile['outfile']):
            extract_gzip(dbfile['outfile'])
            os.remove(dbfile['outfile'])

