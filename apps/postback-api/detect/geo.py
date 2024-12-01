"""Get geo data for an ip address."""
import pathlib
import tarfile
import tempfile

import geoip2.database
import requests
from config import TOP_CONFIGDIR, get_logger

logger = get_logger(__name__)

GITSQUARED_GEOLITE2_RAW_DATA="https://raw.githubusercontent.com/GitSquared/node-geolite2-redist/master/redist/{db}.tar.gz"

MAXMIND_GEO_DBS=["GeoLite2-City", "GeoLite2-ASN"]

def update_geo_dbs()->None:
    """Update the geo databases."""
    for db in MAXMIND_GEO_DBS:
        if pathlib.Path.exists(f"{TOP_CONFIGDIR}/{db}.mmdb"):
            logger.info(f"{db}.mmdb exists, skipping download")
            continue
        logger.info(f"{db}: Unable to find ip geo data")
        logger.info(f"{db}: Downloading {db}.tar.gz")
        url = GITSQUARED_GEOLITE2_RAW_DATA.format(db=db)
        response = requests.get(url, timeout=10)
        logger.info(f"{db}: Unzipping {db}.tar.gz")
        # with open("/tmp/maxmind.tar.gz", "wb") as f:
        with tempfile.NamedTemporaryFile(delete=True) as mytmp:  # Temp file context
            # Write the downloaded content to the temp file
            with pathlib.Path.open(mytmp.name, "wb") as f:
                f.write(response.content)
            logger.info(f"{db}: Write {db}.mmdb to {TOP_CONFIGDIR}")
            # Open the tar file and extract the desired member
            with tarfile.open(mytmp.name, "r:gz") as tar:
                for member in tar.getmembers():
                    if pathlib.Path(member.name).suffix == ".mmdb":
                        with tar.extractfile(member) as r:
                            if r is not None:
                                with pathlib.Path.open(f"{TOP_CONFIGDIR}/{db}.mmdb", "wb") as w:
                                    w.write(r.read())
                                break  # Stop once the target file is written



def lookup_ip(ip:str)->dict:
    """
    Lookup ip address.

    Args:
        ip (str): The ip address to lookup.

    Returns:
        dict: A dictionary containing the geo data for the ip address.

    """
    with geoip2.database.Reader(f"{TOP_CONFIGDIR}/GeoLite2-City.mmdb") as reader:
        response = reader.city(ip)
        country_code = response.country.iso_code
        country_name = response.country.name
        state_code = response.subdivisions.most_specific.iso_code
        state_name = response.subdivisions.most_specific.name
        city_name = response.city.name
        zip_code = response.postal.code
        latitude = response.location.latitude
        longitude = response.location.longitude
        cidr = response.traits.network

    with geoip2.database.Reader(f"{TOP_CONFIGDIR}/GeoLite2-ASN.mmdb") as reader2:
        response2 = reader2.asn(ip)
        asn = response2.autonomous_system_number
        org = response2.autonomous_system_organization
    msg = {
        "country_name":country_name,
        "country_iso":country_code,
        "state_name":state_name,
        "state_iso":state_code,
        "city_name":city_name,
        "zip":zip_code,
        "latitude":latitude,
        "longitude":longitude,
        "cidr":str(cidr),
        "asn":asn,
        "org":org,
    }
    return msg

def get_geo(ip:str)->dict:
    """
    Get geo data for an ip address.

    Args:
        ip (str): The ip address to get geo data for.

    Returns:
        dict: A dictionary containing the geo data for the ip address.

    """
    try:
        msg = lookup_ip(ip)
    except Exception:
        logger.exception(f"failed to get geo info for {ip}")
        msg = {"country_iso":"", "state_iso":"", "city_name":""}
    return msg



get_geo("172.18.0.10")
