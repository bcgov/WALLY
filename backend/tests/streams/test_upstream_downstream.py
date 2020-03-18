import pytest

from api.v1.stream.controller import watershed_root_code

import logging

logger = logging.getLogger('test')


class TestUpstreamDownstream:
    def watershed_root_code(self):
        data = [
            {
                "val": '100-123456-000000-000000-000000-000000',
                "expect": ['100', '123456']
            },
            {
                "val": '100-123456-999999-000000-000000-000000',
                "expect": ['100', '123456', '999999']
            },
            {
                "val": '100-123456-123456-123456-123456-123456',
                "expect": ['100', '123456', '123456', '123456', '123456', '123456']
            }
        ]
        for d in data:
            assert watershed_root_code(d.get('val')) == d.get('expect')
