
import math

import networkx as nx


def information_content(G, term):
    if term not in G.desc_count:
        return
    freq = G.desc_count[term] / len(G)
    return round(-1 * math.log2(freq), 3)


def lowest_common_ancestor(G, term1, term2):
    if not G.desc_count:
        raise ValueError("No pre-calculated desc_count.")
    # Naive implementation of lowest common ancestors
    common_ans = nx.ancestors(G, term1) & nx.ancestors(G, term2)
    if not common_ans:
        return
    return min(common_ans, key=lambda x: G.desc_count.get(x, 0))


def resnik(G, term1, term2):
    """Semantic similarity based on Resnik method
    """
    # TODO: may not work
    # mica = nx.lowest_common_ancestor(G, term1, term2)
    mica = lowest_common_ancestor(G, term1, term2)
    return information_content(G, mica)


def lin(G, term1, term2):
    """Semantic similarity based on Lin method
    """
    ic1 = information_content(G, term1)
    ic2 = information_content(G, term2)
    ic_lca = resnik(G, term1, term2)
    try:
        return round(2 * ic_lca / (ic1 + ic2), 3)
    except TypeError:
        pass


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
    return round(cv / (sva + svb), 3)
