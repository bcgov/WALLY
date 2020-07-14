import geojson
from urllib.parse import parse_qs, urlparse

from api.v1.aggregator.controller import build_api_query
from api.v1.aggregator.schema import WMSGetMapQuery, ExternalAPIRequest
from api.v1.aggregator.excel import xlsx_export, geojson_to_xlsx
from api.v1.aggregator.schema import LayerResponse

OVERLAP_AQUIFERS_HYDAT_LAYER = [-123.0681610107422,
                                49.27430088974207, -122.98387527465822, 49.333176910734124]


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

    resp_object = xlsx_export(datasets)
    assert resp_object.media_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def test_geojson_to_xlsx():
    """ test that the geojson_to_xlsx function returns a saved excel sheet """

    fcstr = """{"type":"FeatureCollection", "properties":{"name": "Hydrometric"}, "features":[{"type":"Feature","id":"71X109JU","geometry":{"type":"Point","coordinates":[-122.98621,49.242402]},"properties":{"name":"Park Creek","type":"hydat","url":"/api/v1/hydat/71X109JU","description":"Stream discharge and water level data"}},{"type":"Feature","id":"7G1TTTIR","geometry":{"type":"Point","coordinates":[-122.944899,49.152419]},"properties":{"name":"Newman Creek","type":"hydat","url":"/api/v1/hydat/7G1TTTIR","description":"Stream discharge and water level data"}},{"type":"Feature","id":"1NPZ1N8K","geometry":{"type":"Point","coordinates":[-123.018208,49.295541]},"properties":{"name":"Jones Creek","type":"hydat","url":"/api/v1/hydat/1NPZ1N8K","description":"Stream discharge and water level data"}},{"type":"Feature","id":"J26OWP2C","geometry":{"type":"Point","coordinates":[-123.054957,49.258437]},"properties":{"name":"Kim Creek","type":"hydat","url":"/api/v1/hydat/J26OWP2C","description":"Stream discharge and water level data"}},{"type":"Feature","id":"WEN80TBJ","geometry":{"type":"Point","coordinates":[-122.999392,49.18851]},"properties":{"name":"Cole Creek","type":"hydat","url":"/api/v1/hydat/WEN80TBJ","description":"Stream discharge and water level data"}},{"type":"Feature","id":"Z54QK60J","geometry":{"type":"Point","coordinates":[-123.008165,49.267485]},"properties":{"name":"Cline Creek","type":"hydat","url":"/api/v1/hydat/Z54QK60J","description":"Stream discharge and water level data"}},{"type":"Feature","id":"H8MA1VGB","geometry":{"type":"Point","coordinates":[-122.943351,49.250503]},"properties":{"name":"Hooper Creek","type":"hydat","url":"/api/v1/hydat/H8MA1VGB","description":"Stream discharge and water level data"}}]}"""
    fc = geojson.loads(fcstr)

    datasets = [fc]

    resp_object = geojson_to_xlsx(datasets)
    assert resp_object.media_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
