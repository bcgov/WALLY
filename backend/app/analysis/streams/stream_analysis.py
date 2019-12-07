import json
import logging
import requests
from sqlalchemy import func
from sqlalchemy.orm import Session, load_only
from app.aggregator.endpoints import API_DATASOURCES
from app.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from geoalchemy2.shape import to_shape
from geojson import Feature
from shapely import wkb

logger = logging.getLogger("api")

def get_connected_streams(db: Session, outflowCode: str) -> list:

    # q = db.query(
    #     FreshwaterAtlasStreamNetworks.OGC_FID,
    #     FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE,
    #     FreshwaterAtlasStreamNetworks.DOWNSTREAM_ROUTE_MEASURE,
    #     FreshwaterAtlasStreamNetworks.LOCAL_WATERSHED_CODE,
    #     FreshwaterAtlasStreamNetworks.GEOMETRY,
    # ) \
    #     .filter(FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.startswith(outflowCode))

    q = db.query(FreshwaterAtlasStreamNetworks) \
        .filter(FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.startswith(outflowCode))

    results = q.all()

    # results = db.execute('select "OGC_FID", "FWA_WATERSHED_CODE", "DOWNSTREAM_ROUTE_MEASURE", \
    #     "LOCAL_WATERSHED_CODE", "GEOMETRY" from freshwater_atlas_stream_networks where \
    #     "FWA_WATERSHED_CODE" >= :code;', {'code': outflowCode})

    # feature_results = []
    # for row in enumerate(results):
    #     data = row[1]
    #     feature = Feature(
    #         id=data[0],
    #         properties={
    #             'FWA_WATERSHED_CODE': data[1],
    #             'DOWNSTREAM_ROUTE_MEASURE': data[2],
    #             'LOCAL_WATERSHED_CODE': data[3],
    #         },
    #         # geometry=to_shape(data[4])
    #         geometry=wkb.loads(data[4], hex=True)
    #     )
    #     feature_results.append(feature)

    # feature_results = [Feature(
    #         id=getattr(row, 'OGC_FID'),
    #         properties={**row.__dict__},
    #         geometry=to_shape(getattr(row, 'GEOMETRY'))
    #     ) for row in results]

    # feature_results = [FreshwaterAtlasStreamNetworks(**row.__dict__) for row in results]

    feature_results = [FreshwaterAtlasStreamNetworks \
        .get_as_feature(row, FreshwaterAtlasStreamNetworks.GEOMETRY) for row in results]

    # logger.info(feature_results)

    return feature_results


def get_features_within_buffer(db: Session, geometry, buffer: float, layer: str) -> list:
    """ List features within a buffer zone from a geometry
    """
    layer_class = API_DATASOURCES[layer]
    geom = layer_class.get_geom_column(db)

    feature_results = db.query(
        layer_class,
        func.ST_Distance(func.Geography(geom),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(geom),
                            func.ST_GeographyFromText(geometry.wkt), buffer)
    ) \
    .order_by('distance').all()

    features = [layer_class.get_as_properties(row[0]) for row in feature_results]

    return features
