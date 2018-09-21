
from pathlib import Path
import re

import networkx as nx

from pygosemsim import exception


resource_dir = Path(__file__).resolve().parent / "_resources"

termdef = re.compile(r"^\[([a-zA-Z_]+?)\]$")
splitkv = re.compile(r"(^[a-zA-Z_]+): (.+)")


class GoGraph(nx.DiGraph):
    """Directed acyclic graph of Gene Ontology

    Attributes:
        alt_ids(dict): alternative IDs dictionary
        descriptors(set): flags and tokens that indicates the graph is
            specialized for some kind of analyses
        lower_bounds(collections.Counter):
            Pre-calculated lower bound count (Number of descendants + 1).
            Information content calculation requires precalc lower bounds.
            see `pygosemsim.similarity.precalc_lower_bounds`
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alt_ids = {}  # Alternative IDs
        self.descriptors = set()
        self.lower_bounds = None
        # self.reversed = self.reverse(copy=False)

    def require(self, desc):
        if desc not in self.descriptors:
            raise exception.PGSSInvalidOperation(
                "'{}' is required.".format(desc))


def parse_block(lines):
    """Parse a Term block
    """
    term = {
        "alt_id": [],
        "relationship": []
    }
    for line in lines:
        m = re.search(splitkv, line)
        assert m, f"unexpected line: {line}"
        key = m.group(1)
        value = m.group(2)
        if key in ["id", "name", "namespace", "is_obsolete"]:
            term[key] = value
        elif key == "alt_id":
            term["alt_id"].append(value)
        elif key == "is_a":
            goid = value.split("!")[0].strip()
            term["relationship"].append({"type": "is_a", "id": goid})
        elif key == "relationship":
            typedef, goid = value.split("!")[0].strip().split(" ")
            term["relationship"].append({"type": typedef, "id": goid})
    assert "id" in term, "missing id"
    assert "name" in term, "missing name"
    assert "namespace" in term, "missing namespace"
    return term


def blocks_iter(lines):
    """Iterate Term (and Typedef) blocks
    """
    type_ = None
    content = []
    for line in lines:
        m = re.search(termdef, line)
        if m:
            if type_ is not None and content:
                yield {"type": type_, "content": content[:]}
            type_ = m.group(1)
            content.clear()
        elif line.rstrip():
            content.append(line.rstrip())
    if content:
        yield {"type": type_, "content": content[:]}


def from_obo_lines(lines, ignore_obsolete=True):
    lines_iter = iter(lines)

    # Header
    fv_line = next(lines_iter)
    format_ver = fv_line.split(":")[1].strip()
    print(f"format-version: {format_ver}")

    # Build graph
    G = GoGraph()
    alt_ids = set()

    # Term blocks
    for tb in blocks_iter(lines_iter):
        if tb["type"] != "Term":
            assert tb["type"] == "Typedef", f"unexpected type {tb['type']}"
            continue
        term = parse_block(tb["content"])

        # Ignore obsolete term
        obso = term.get("is_obsolete") == "true"
        if obso and ignore_obsolete:
            continue

        # Alternative ID mapping
        alt_ids |= set(term["alt_id"])
        for alt_id in term["alt_id"]:
            G.alt_ids[alt_id] = term["id"]

        # Add node
        attr = {
            "name": term["name"],
            "namespace": term["namespace"],
            "is_obsolete": obso
        }
        G.add_node(term["id"], **attr)
        for rel in term["relationship"]:
            G.add_edge(rel["id"], term["id"], type=rel["type"])

    # Check
    assert not (set(G) & alt_ids), "Inconsistent alternative IDs"
    assert len(G) >= 2, "The graph size is too small"
    assert G.number_of_edges(), "The graph has no edges"

    return G


def from_obo(pathlike, **kwargs):
    with open(pathlike, "rt") as f:
        G = from_obo_lines(f, **kwargs)
    return G


def from_resource(name, **kwargs):
    filename = f"{name}.obo"
    return from_obo(resource_dir / filename, **kwargs)
