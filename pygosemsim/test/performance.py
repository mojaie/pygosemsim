#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import functools
import unittest

import networkx as nx

from pygosemsim import annotation, graph, similarity, term_set
from pygosemsim.util import debug


class TestPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.G = graph.from_resource("go-basic")
        graph.precalc_descendants(cls.G)
        cls.annot = annotation.from_resource("goa_human")

    def test_similarity(self):
        similarity.resnik(self.G, "GO:0004340", "GO:0019158")
        similarity.wang(self.G, "GO:0004340", "GO:0019158")

    @debug.profile
    def test_term_set(self):
        trpv1 = self.annot["Q8NER1"]["annotation"].keys()
        trpa1 = self.annot["O75762"]["annotation"].keys()
        sf = functools.partial(term_set.sim_func, self.G, similarity.lin)
        print(term_set.sim_bma(trpv1, trpa1, sf))
