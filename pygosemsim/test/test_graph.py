#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import unittest

import networkx as nx

from pygosemsim import graph

@unittest.skip("")
class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.G = graph.from_resource("goslim_chembl")
        graph.precalc_descendants(cls.G)

    def test_graph(self):
        self.G.desc_count["GO:0004340"]
        self.G.desc_count["GO:0004396"]
        self.G.desc_count["GO:0016301"]
