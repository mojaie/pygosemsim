#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import unittest

from pygosemsim import graph, similarity


class TestSimilarity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.G = graph.from_resource("goslim_chembl")
        graph.precalc_descendants(cls.G)

    def test_similarity(self):
        similarity.resnik(self.G, "GO:0004340", "GO:0019158")
        similarity.wang(self.G, "GO:0004340", "GO:0019158")
        similarity.norm_resnik(self.G, "GO:0004340", "GO:0019158")
        similarity.norm_resnik(self.G, "GO:0004340", "GO:0016301")
        similarity.norm_resnik(self.G, "GO:0016301", "GO:0016301")
