from astro.geo import Location
import pytest

from astro.lib import Astro


@pytest.fixture
def manual_astro():
    return Astro.from_args(lat=-34.2, lon=-57.3)
