# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import unicode_literals
from __future__ import division

import base_test_class
from tests.base_test_class import ActiveDataBaseTest



class TestAggOps(ActiveDataBaseTest):

    def test_simplest(self):
        test = {
            "data": [{"a": i} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"aggregate": "count"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 30
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["count"],
                "data": [[30]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "count": 30
                }
            }
        }
        self._execute_es_tests(test)

    def test_max(self):
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"value": "a", "aggregate": "max"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 58
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[58]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": 58
                }
            }
        }
        self._execute_es_tests(test)


    def test_median(self):
        test = {
            "data": [{"a": i**2} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"value": "a", "aggregate": "median"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 210.5
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[210.5]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": 210.5
                }
            }
        }
        self._execute_es_tests(test)


    def test_percentile(self):
        test = {
            "data": [{"a": i**2} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"value": "a", "aggregate": "percentile", "percentile": 0.90}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 681.3
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[681.3]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": 681.3
                }
            }
        }
        self._execute_es_tests(test)


    def test_many_aggs_on_one_column(self):
        # ES WILL NOT ACCEPT TWO (NAIVE) AGGREGATES ON SAME FIELD, COMBINE THEM USING stats AGGREGATION
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": [
                    {"name": "maxi", "value": "a", "aggregate": "max"},
                    {"name": "mini", "value": "a", "aggregate": "min"},
                    {"name": "count", "value": "a", "aggregate": "count"}
                ]
            },
            "expecting_list": {
                "meta": {"format": "value"},
                "data": {"mini": 0, "maxi": 58, "count": 30}
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["mini", "maxi", "count"],
                "data": [
                    [0, 58, 30]
                ]
            }
        }
        self._execute_es_tests(test)


    def test_simplest_on_value(self):
        test = {
            "data": range(30),
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"aggregate": "count"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 30
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["count"],
                "data": [[30]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "count": 30
                }
            }
        }
        self._execute_es_tests(test, tjson=True)

    def test_max_on_value(self):
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"value": ".", "aggregate": "max"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 58
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["max"],
                "data": [[58]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "max": 58
                }
            }
        }
        self._execute_es_tests(test, tjson=True)


    def test_max_object_on_value(self):
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": [{"value": ".", "aggregate": "max"}]
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": {"max": 58}
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["max"],
                "data": [[58]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "max": 58
                }
            }
        }
        self._execute_es_tests(test, tjson=True)


    def test_median_on_value(self):
        test = {
            "data": [i**2 for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": {"value": ".", "aggregate": "median"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 210.5
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["median"],
                "data": [[210.5]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "median": 210.5
                }
            }
        }
        self._execute_es_tests(test, tjson=True)


    def test_many_aggs_on_value(self):
        # ES WILL NOT ACCEPT TWO (NAIVE) AGGREGATES ON SAME FIELD, COMBINE THEM USING stats AGGREGATION
        test = {
            "data": [i*2 for i in range(30)],
            "query": {
                "from": base_test_class.settings.backend_es.index,
                "select": [
                    {"name": "maxi", "value": ".", "aggregate": "max"},
                    {"name": "mini", "value": ".", "aggregate": "min"},
                    {"name": "count", "value": ".", "aggregate": "count"}
                ]
            },
            "expecting_list": {
                "meta": {"format": "value"},
                "data": {"mini": 0, "maxi": 58, "count": 30}
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["mini", "maxi", "count"],
                "data": [
                    [0, 58, 30]
                ]
            }
        }
        self._execute_es_tests(test, tjson=True)

