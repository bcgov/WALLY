from urllib.parse import parse_qs, urlparse

from app.aggregator.aggregate import form_wms_query
from app.aggregator.models import WMSGetMapQuery, WMSRequest


def test_wms_url():
    """ test that the WMS URL is formed properly """

    layer_q = WMSGetMapQuery(
        request="GetMap",
        service="WMS",
        srs="EPSG:4326",
        version="1.1.1",
        format="application/json;type=topojson",
        bbox="-125.99807739257814,53.86062638824399,-125.46661376953126,54.10893027534094",
        height=1243,
        width=1445,
        layers="WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
    )

    layer = WMSRequest(
        url="https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?",
        q=layer_q
    )

    expected_url = """https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?request=GetMap&service=WMS&srs=EPSG%3A4326&version=1.1.1&format=application%2Fjson%3Btype%3Dtopojson&bbox=-125.99807739257814%2C53.86062638824399%2C-125.46661376953126%2C54.10893027534094&height=1243&width=1445&layers=WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW"""

    # check that the URL formed by the function is in the correct format (matches the one
    # known to work). Since the query string params might not be in the same order,
    # parse the queries to a dict before comparing.
    q1 = urlparse(form_wms_query(layer)).query
    q2 = urlparse(expected_url).query

    dict1 = parse_qs(q1)
    dict2 = parse_qs(q2)

    assert dict1 == dict2
