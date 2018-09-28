#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import unittest

from pygosemsim import exception, graph, similarity


class TestSimilarity(unittest.TestCase):
    def test_lca(self):
        G = graph.GoGraph()
        G.add_nodes_from(range(15))
        G.add_edges_from([
            (0, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
            (0, 2), (2, 8), (8, 9), (9, 3), (2, 10), (10, 11), (11, 4),
            (12, 13), (13, 14)
        ])

        # No pre-calculated desc_count
        with self.assertRaises(exception.PGSSInvalidOperation):
            similarity.lowest_common_ancestor(G, 6, 7)
        with self.assertRaises(exception.PGSSInvalidOperation):
            similarity.information_content(G, 6)

        # Graph 1
        similarity.precalc_lower_bounds(G)
        self.assertEqual(G.lower_bounds[0], 12)
        self.assertEqual(similarity.lowest_common_ancestor(G, 6, 7), 1)
        self.assertEqual(G.lower_bounds[1], 6)
        self.assertEqual(G.lower_bounds[2], 7)
        self.assertEqual(similarity.lowest_common_ancestor(G, 3, 4), 1)
        self.assertEqual(similarity.resnik(G, 3, 4), 1.322)
        self.assertEqual(similarity.pekar(G, 3, 4), 0.333)
        # Direct ancestor/descendant
        self.assertEqual(similarity.lowest_common_ancestor(G, 12, 14), 12)
        # No common ancestors
        self.assertEqual(similarity.lowest_common_ancestor(G, 7, 13), None)
        self.assertEqual(similarity.resnik(G, 7, 13), None)
        # Missing node
        with self.assertRaises(exception.PGSSLookupError):
            similarity.lowest_common_ancestor(G, 6, 18)

        # Graph 2
        G.add_edge(7, 12)
        similarity.precalc_lower_bounds(G)
        self.assertEqual(G.lower_bounds[1], 9)
        self.assertEqual(similarity.lowest_common_ancestor(G, 3, 4), 2)
        self.assertEqual(similarity.resnik(G, 3, 4), 1.1)
        self.assertEqual(similarity.norm_resnik(G, 3, 4), 0.282)
        self.assertEqual(similarity.pekar(G, 3, 4), 0.143)
        # Information content
        self.assertEqual(similarity.information_content(G, 6), 3.907)
        self.assertEqual(similarity.information_content(G, 0), 0)
        # Missing node
        with self.assertRaises(exception.PGSSLookupError):
            similarity.information_content(G, 18)
        # Root node
        self.assertEqual(similarity.lowest_common_ancestor(G, 0, 0), 0)
        self.assertEqual(similarity.resnik(G, 0, 0), 0)
        self.assertEqual(similarity.norm_resnik(G, 0, 0), 0)
        self.assertEqual(similarity.pekar(G, 0, 0), None)
        self.assertEqual(similarity.lin(G, 0, 0), None)  # Zero division




    """
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
    """
