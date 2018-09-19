
import math

import networkx as nx


def information_content(G, term):
    freq = (len(nx.descendants(G, term)) + 1) / len(G)
    return -1 * math.log2(freq)


def resnik(G, term1, term2):
    """Semantic similarity based on Resnik method
    """
    lca = nx.lowest_common_ancestor(G, term1, term2)
    if lca is None:
        raise ValueError("No common ancestor")
    return information_content(G, lca)


def lin(G, term1, term2):
    """Semantic similarity based on Lin method
    """
    ic1 = information_content(G, term1)
    ic2 = information_content(G, term2)
    ic_lca = resnik(G, term1, term2)
    return 2 * ic_lca / (ic1 + ic2)


default_wf = (("is_a", 0.8), ("part_of", 0.6))


def s_values(G, term, weight_factor=default_wf):
    wf = dict(weight_factor)
    sv = {term: 1}
    visited = set()
    level = {term}
    while level:
        visited |= level
        next_level = set()
        for n in level:
            for pred, edge in G.pred[n].items():
                weight = sv[n] * wf.get(edge["type"], 0)
                if pred not in sv:
                    sv[pred] = weight
                else:
                    sv[pred] = max([sv[pred], weight])
                if pred not in visited:
                    next_level.add(pred)
        level = next_level
    return {k: round(v, 3) for k, v in sv.items()}


def wang(G, term1, term2, weight_factor=default_wf):
    """Semantic similarity based on Wang method
    """
    s1 = s_values(G, term1, weight_factor)
    s2 = s_values(G, term2, weight_factor)
    sva = sum(s1.values())
    svb = sum(s2.values())
    common = set(s1.keys()) & set(s2.keys())
    cv = sum(s1[c] + s2[c] for c in common)
    return cv / (sva + svb)
