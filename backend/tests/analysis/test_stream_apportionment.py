import random
import pytest

from app.v1.controllers.streams import get_apportionment, get_inverse_distance
import logging

logger = logging.getLogger('test')


class TestStreamApportionment:
    def test_apportionment(self):
        data = [
            {
                'distance': 5,
                'weighting_factor': 2,
                'inverse_distance': 0.04
            },
            {
                'distance': 10,
                'weighting_factor': 3,
                'inverse_distance': 0.001
            },
            {
                'distance': 10,
                'weighting_factor': 2,
                'inverse_distance': 0.01
            }]
        for d in data:
            x = get_inverse_distance(d['distance'], d['weighting_factor'])
            assert d['inverse_distance'] == x

    def test_streams_with_apportionment(self):
        data = [{
            'weighting_factor': 2,
            'nearby_streams': [
                {
                    'distance': 5
                },
                {
                    'distance': 6
                },
                {
                    'distance': 16
                }
            ],
            'streams_with_apportionment': [
                {
                    'distance': 5,
                    'apportionment': 59.01639344262296
                },
                {
                    'distance': 6,
                    'apportionment': 40.98360655737705
                },
            ]
        }, {
            'weighting_factor': 2,
            'nearby_streams': [
                                   {
                                   'distance': 50
                                   },
                                   {
                                   'distance': 60
                                   },
                                   {
                                   'distance': 160
                                   }
                                      ],
            'streams_with_apportionment': [
                {
                    'distance': 50,
                    'apportionment': 59.016392
                },
                {
                    'distance': 60,
                    'apportionment': 40.983608
                },
            ]
        }, {
            'weighting_factor': 3,
            'nearby_streams': [
                                   {
                                   'distance': 5
                                   },
                                   {
                                   'distance': 6
                                   },
                                   {
                                   'distance': 16
                                   }
                                      ],
            'streams_with_apportionment': [
                {
                    'distance': 5,
                    'inverse_distance': 0.000008,
                    'apportionment': 63.34
                },
                {
                    'distance': 6,
                    'apportionment': 36.66
                },
            ]
        }, {
            'weighting_factor': 2,
            'nearby_streams': [
                                   {
                                   'distance': 20
                                   },
                                   {
                                   'distance': 4
                                   },
                                   {
                                   'distance': 2
                                   }
                                      ],
            'streams_with_apportionment': [
                {
                    'distance': 4,
                    'apportionment': 20
                },
                {
                    'distance': 2,
                    'apportionment': 80
                },
            ]
        }]

        for d in data:
            streams = get_apportionment(d['nearby_streams'], d['weighting_factor'])
            assert len(streams) == len(d['streams_with_apportionment'])
            for i, stream in enumerate(streams):
                assert round(stream['apportionment'], 2) == round(d['streams_with_apportionment'][i]['apportionment'], 2)

    def test_compute_exceed_10_streams(self):
        streams = [{'distance': random.randrange(50, 300)} for i in range(15)]
        with pytest.raises(RecursionError):
            streams_with_apportionment = get_apportionment(streams, 2)

        streams = [{'distance': random.randrange(50, 300)} for i in range(11)]
        with pytest.raises(RecursionError):
            streams_with_apportionment = get_apportionment(streams, 2)

    def test_force_compute_more_than_10_streams(self):
        streams = [{'distance': random.randrange(50, 300)} for i in range(11)]
        streams_with_apportionment = get_apportionment(streams, 2, force_recursion=True)
        assert len(streams_with_apportionment) > 0

    def test_keep_streams_with_less_than_10_percent_apportionment(self):
        streams = [{'distance': random.randrange(50, 300)} for i in range(10)]
        streams_with_apportionment = get_apportionment(streams, 2, get_all=True)
        assert len(streams) == len(streams_with_apportionment)

