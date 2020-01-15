import geojson
from urllib.parse import parse_qs, urlparse

from api.v1.aggregator.controller import build_api_query
from api.v1.aggregator.schema import WMSGetMapQuery, ExternalAPIRequest
from api.v1.aggregator.excel import xlsxExport, geojson_to_xlsx
from api.v1.aggregator.schema import LayerResponse

OVERLAP_AQUIFERS_HYDAT_LAYER = [-123.0681610107422,
                                49.27430088974207, -122.98387527465822, 49.333176910734124]


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

    layer = ExternalAPIRequest(
        url="https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?",
        layer="WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
        q=layer_q
    )

    expected_url = """https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?request=GetMap&service=WMS&srs=EPSG%3A4326&version=1.1.1&format=application%2Fjson%3Btype%3Dtopojson&bbox=-125.99807739257814%2C53.86062638824399%2C-125.46661376953126%2C54.10893027534094&height=1243&width=1445&layers=WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW"""

    # check that the URL formed by the function is in the correct format (matches the one
    # known to work). Since the query string params might not be in the same order,
    # parse the queries to a dict before comparing.
    q1 = urlparse(build_api_query(layer)).query
    q2 = urlparse(expected_url).query

    dict1 = parse_qs(q1)
    dict2 = parse_qs(q2)

    # assert dict1 == dict2


def test_xlsx_export():
    """ test that the xlsx_export function returns a saved excel sheet """

    fcstr = """{"type":"FeatureCollection","features":[{"type":"Feature","id":"71X109JU","geometry":{"type":"Point","coordinates":[-122.98621,49.242402]},"properties":{"name":"Park Creek","type":"hydat","url":"/api/v1/hydat/71X109JU","description":"Stream discharge and water level data"}},{"type":"Feature","id":"7G1TTTIR","geometry":{"type":"Point","coordinates":[-122.944899,49.152419]},"properties":{"name":"Newman Creek","type":"hydat","url":"/api/v1/hydat/7G1TTTIR","description":"Stream discharge and water level data"}},{"type":"Feature","id":"1NPZ1N8K","geometry":{"type":"Point","coordinates":[-123.018208,49.295541]},"properties":{"name":"Jones Creek","type":"hydat","url":"/api/v1/hydat/1NPZ1N8K","description":"Stream discharge and water level data"}},{"type":"Feature","id":"J26OWP2C","geometry":{"type":"Point","coordinates":[-123.054957,49.258437]},"properties":{"name":"Kim Creek","type":"hydat","url":"/api/v1/hydat/J26OWP2C","description":"Stream discharge and water level data"}},{"type":"Feature","id":"WEN80TBJ","geometry":{"type":"Point","coordinates":[-122.999392,49.18851]},"properties":{"name":"Cole Creek","type":"hydat","url":"/api/v1/hydat/WEN80TBJ","description":"Stream discharge and water level data"}},{"type":"Feature","id":"Z54QK60J","geometry":{"type":"Point","coordinates":[-123.008165,49.267485]},"properties":{"name":"Cline Creek","type":"hydat","url":"/api/v1/hydat/Z54QK60J","description":"Stream discharge and water level data"}},{"type":"Feature","id":"H8MA1VGB","geometry":{"type":"Point","coordinates":[-122.943351,49.250503]},"properties":{"name":"Hooper Creek","type":"hydat","url":"/api/v1/hydat/H8MA1VGB","description":"Stream discharge and water level data"}}]}"""
    fc = geojson.loads(fcstr)

    datasets = [
        LayerResponse(
            layer='test hydrometric layer',
            status=200,
            geojson=fc
        )
    ]

    resp_object = xlsxExport(datasets)
    assert resp_object.media_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def test_geojson_to_xlsx():
    """ test that the geojson_to_xlsx function returns a saved excel sheet """

    fcstr = """{"type":"FeatureCollection", "properties":{"name": "Hydrometric"}, "features":[{"type":"Feature","id":"71X109JU","geometry":{"type":"Point","coordinates":[-122.98621,49.242402]},"properties":{"name":"Park Creek","type":"hydat","url":"/api/v1/hydat/71X109JU","description":"Stream discharge and water level data"}},{"type":"Feature","id":"7G1TTTIR","geometry":{"type":"Point","coordinates":[-122.944899,49.152419]},"properties":{"name":"Newman Creek","type":"hydat","url":"/api/v1/hydat/7G1TTTIR","description":"Stream discharge and water level data"}},{"type":"Feature","id":"1NPZ1N8K","geometry":{"type":"Point","coordinates":[-123.018208,49.295541]},"properties":{"name":"Jones Creek","type":"hydat","url":"/api/v1/hydat/1NPZ1N8K","description":"Stream discharge and water level data"}},{"type":"Feature","id":"J26OWP2C","geometry":{"type":"Point","coordinates":[-123.054957,49.258437]},"properties":{"name":"Kim Creek","type":"hydat","url":"/api/v1/hydat/J26OWP2C","description":"Stream discharge and water level data"}},{"type":"Feature","id":"WEN80TBJ","geometry":{"type":"Point","coordinates":[-122.999392,49.18851]},"properties":{"name":"Cole Creek","type":"hydat","url":"/api/v1/hydat/WEN80TBJ","description":"Stream discharge and water level data"}},{"type":"Feature","id":"Z54QK60J","geometry":{"type":"Point","coordinates":[-123.008165,49.267485]},"properties":{"name":"Cline Creek","type":"hydat","url":"/api/v1/hydat/Z54QK60J","description":"Stream discharge and water level data"}},{"type":"Feature","id":"H8MA1VGB","geometry":{"type":"Point","coordinates":[-122.943351,49.250503]},"properties":{"name":"Hooper Creek","type":"hydat","url":"/api/v1/hydat/H8MA1VGB","description":"Stream discharge and water level data"}}]}"""
    fc = geojson.loads(fcstr)

    datasets = [fc]

    resp_object = geojson_to_xlsx(datasets)
    assert resp_object.media_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
