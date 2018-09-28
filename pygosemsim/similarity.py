
from collections import Counter
import math

import networkx as nx

from pygosemsim import exception


def precalc_lower_bounds(G):
    """Pre-calculate the number of lower bounds of the graph nodes
    """
    G.lower_bounds = Counter()
    for n in G:
        G.lower_bounds[n] += 1
        for ans in nx.ancestors(G, n):
            G.lower_bounds[ans] += 1
    G.descriptors.add("Pre-calculated lower bounds")


def information_content(G, term):
    """Information content

    Args:
        G(GoGraph): GoGraph object
        term(str): GO term

    Returns:
        str - Information content

    Raises:
        PGSSLookupError: The term was not found in GoGraph
        PGSSInvalidOperation: see `pygosemsim.similarity.precalc_lower_bounds`
    """
    G.require("Pre-calculated lower bounds")
    if term not in G.lower_bounds:
        raise exception.PGSSLookupError(f"Missing term: {term}")
    freq = G.lower_bounds[term] / len(G)
    return round(-1 * math.log2(freq), 3)


def lowest_common_ancestor(G, term1, term2):
    """Naive implementation of lowest common ancestor (LCA)

    Args:
        G(GoGraph): GoGraph object
        term1(str): GO term
        term2(str): GO term

    Returns:
        str - Lowest common ancestor term
        or None if the terms have no common ancestors

    Raises:
        PGSSLookupError: The term was not found in GoGraph
        PGSSInvalidOperation: see `pygosemsim.similarity.precalc_lower_bounds`
    """
    G.require("Pre-calculated lower bounds")
    if term1 not in G:
        raise exception.PGSSLookupError(f"Missing term: {term1}")
    if term2 not in G:
        raise exception.PGSSLookupError(f"Missing term: {term2}")
    lb1 = nx.ancestors(G, term1) | {term1}
    lb2 = nx.ancestors(G, term2) | {term2}
    common_ans = lb1 & lb2
    if not common_ans:
        return
    return min(common_ans, key=lambda x: G.lower_bounds[x])


def resnik(G, term1, term2):
    """Semantic similarity based on Resnik method

    Args:
        G(GoGraph): GoGraph object
        term1(str): GO term
        term2(str): GO term

    Returns:
        float - Resnik similarity value (Information content of LCA)
        or None if the terms have no common ancestors

    Raises:
        PGSSLookupError: The term was not found in GoGraph
        PGSSInvalidOperation: see `pygosemsim.similarity.precalc_lower_bounds`
    """
    # TODO: may not work
    # mica = nx.lowest_common_ancestor(G, term1, term2)
    mica = lowest_common_ancestor(G, term1, term2)
    if mica is not None:
        return information_content(G, mica)


def norm_resnik(G, term1, term2):
    """Semantic similarity based on Resnik method.
    Information content of theoretically the most rare word (with frequency
    of 1 / corpus size) is used for normalization.

    Args:
        G(GoGraph): GoGraph object
        term1(str): GO term
        term2(str): GO term

    Returns:
        float - Normalized Resnik similarity in the range of 0 to 1
        or None if the terms have no common ancestors

    Raises:
        PGSSLookupError: The term was not found in GoGraph
        PGSSInvalidOperation: see `pygosemsim.similarity.precalc_lower_bounds`
    """
    max_ic = -1 * math.log2(1 / len(G))
    res = resnik(G, term1, term2)
    if res is None:
        return
    return round(res / max_ic, 3)


def lin(G, term1, term2):
    """Semantic similarity based on Lin method.

    Args:
        G(GoGraph): GoGraph object
        term1(str): GO term
        term2(str): GO term

    Returns:
        float - Lin similarity
        returns None if the terms have no common ancestors
        returns None if both term1 and term2 are the root term

    Raises:
        PGSSLookupError: The term was not found in GoGraph
        PGSSInvalidOperation: see `pygosemsim.similarity.precalc_lower_bounds`
    """
    ic1 = information_content(G, term1)
    ic2 = information_content(G, term2)
    ic_lca = resnik(G, term1, term2)
    try:
        return round(2 * ic_lca / (ic1 + ic2), 3)
    except (TypeError, ZeroDivisionError):
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

    Args:
        G(GoGraph): GoGraph object
        term1(str): GO term
        term2(str): GO term
        weight_factor(tuple): custom weight factor params

    Returns:
        float - Wang similarity value

    Raises:
        PGSSLookupError: The term was not found in GoGraph
    """
    if term1 not in G:
        raise exception.PGSSLookupError(f"Missing term: {term1}")
    if term2 not in G:
        raise exception.PGSSLookupError(f"Missing term: {term2}")
    sa = s_values(G, term1, weight_factor)
    sb = s_values(G, term2, weight_factor)
    sva = sum(sa.values())
    svb = sum(sb.values())
    common = set(sa.keys()) & set(sb.keys())
    cv = sum(sa[c] + sb[c] for c in common)
    return round(cv / (sva + svb), 3)


def pekar(G, term1, term2):
    """Edge-based similarity based on the method by Pekar et al.
    The original study deals with tree-structured taxonomy.
    In the context of DAG, LCA is defined as the node that have
    the lowest number of descendant terms.

    Args:
        G(GoGraph): GoGraph object
        term1(str): GO term
        term2(str): GO term

    Returns:
        float - similarity value
        returns None if both term1 and term2 are the root term

    Raises:
        PGSSLookupError: The term was not found in GoGraph
        PGSSInvalidOperation: see `pygosemsim.similarity.precalc_lower_bounds`
    """
    # TODO: not optimized yet
    mica = lowest_common_ancestor(G, term1, term2)
    ac = nx.shortest_path_length(G, source=mica, target=term1)
    bc = nx.shortest_path_length(G, source=mica, target=term2)
    root = max(nx.ancestors(G, mica),
               key=lambda x: G.lower_bounds[x], default=mica)
    rootc = nx.shortest_path_length(G, source=root, target=mica)
    try:
        return round(rootc / (ac + bc + rootc), 3)
    except ZeroDivisionError:
        pass
