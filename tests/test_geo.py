import pytest
import pytz
from unittest import mock

from astro.geo import IPInfoLocation, Location


@pytest.mark.parametrize(
    "use_cache,request_called",
    [
        (True, False),
        (False, True),
    ],
)
@mock.patch("astro.geo.cache")
@mock.patch("astro.geo.request")
def test_ipinfo_location(request, cache, use_cache, request_called):
    result = b'{\n  "ip": "181.140.95.129",\n  "hostname": "129-95-170-181.fibertel.com.ar",\n  "city": "La Plata",\n  "region": "Buenos Aires",\n  "country": "AR",\n  "loc": "-34.1215,-57.1545",\n  "org": "AS7303 Telecom Argentina S.A.",\n  "postal": "1900",\n  "timezone": "America/Argentina/Buenos_Aires",\n  "readme": "https://ipinfo.io/missingauth"\n}'
    cache.get.return_value = result
    request.urlopen().read.return_value = result

    loc = IPInfoLocation.from_ip(use_cache=use_cache)

    assert loc.lat == -34.1215
    assert loc.lon == -57.1545
    assert loc.name == "La Plata, Buenos Aires, AR (181.140.95.129)"
    assert loc.tz == pytz.timezone("America/Argentina/Buenos_Aires")

    assert cache.get.called == use_cache
    assert request.urlopen().read.called == request_called
