
pygosemsim
===================================================

**pygosemsim** is a GO (Gene Ontology) semantic similarity calculation library for Python.



Getting started
------------------


### Install


### Download GO datasets and build GO graph

```pycon
>>> from pygosemsim import download

>>> # Download from http://purl.obolibrary.org/
>>> download.obo("go-basic")
Download started: http://purl.obolibrary.org/obo/go/go-basic.obo
Downloaded 32.2MB of 32.2MB (100.0 %)
Download finished: go-basic.obo (32.2) MB

>>> # Or manually
>>> download.download("goslim_chembl.obo",
>>>     "http://www.geneontology.org/ontology/subsets/goslim_chembl.obo")
Download started: http://www.geneontology.org/ontology/subsets/goslim_chembl.obo
Downloaded 0.5MB of 0.5MB (100.0 %)
Download finished: goslim_chembl.obo (0.5) MB

>>> from pygosemsim import graph
>>> import networkx as nx
>>> G = graph.from_resource("go-basic")
format-version: 1.2

>>> G_chembl = graph.from_resource("goslim_chembl")
format-version: 1.2

>>> nx.ancestors(G, "GO:0004396")
{'GO:0003674', 'GO:0003824', 'GO:0016301', 'GO:0016740', 'GO:0016772', 'GO:0016773', 'GO:0019200'}

>>> nx.descendants(G, "GO:0004396")
{'GO:0004340', 'GO:0008865', 'GO:0019158'}
```


### GO term semantic similarity

```pycon
>>> from pygosemsim import similarity
>>> graph.precalc_lower_bounds(G)

>>> similarity.resnik(G, "GO:0004340", "GO:0019158")
13.459

>>> similarity.wang(G, "GO:0004340", "GO:0019158")
0.804
```


### Download and parse gene annotation file

```pycon
>>> download.gaf("goa_human")
Download started: http://geneontology.org/gene-associations/goa_human.gaf.gz
Downloaded 7.9MB of 7.9MB (100.0 %)
Download finished: goa_human.gaf.gz (7.9) MB

>>> from pygosemsim import annotation
>>> annot = annotation.from_resource("goa_human")
gaf-version: 2.1

>>> len(annot)  # Number of genes annotated
19712

>>> annot["Q8NER1"]
{
  'db_object_id': 'Q8NER1',
  'db_object_name': 'Transient receptor potential cation channel subfamily V member 1',
  'db_object_symbol': 'TRPV1',
  'db_object_type': 'protein'
  'annotation': {
    'GO:0000122': {
      'evidence_code': 'IEA',
      'go_id': 'GO:0000122',
      'qualifier': ['']
    },
    'GO:0001660': {
      'evidence_code': 'IEA',
      'go_id': 'GO:0001660',
      'qualifier': ['']
    },
    ...
  }
}
```


### Gene similarity

```pycon
>>> import functools
>>> from pygosemsim import term_set
>>> trpv1 = annot["Q8NER1"]["annotation"].keys()
>>> trpa1 = annot["O75762"]["annotation"].keys()
>>> sf = functools.partial(term_set.sim_func, self.G, similarity.lin)
>>> term_set.sim_bma(trpv1, trpa1, sf)
0.667
```


Features
----------

- File parsers (.obo, .gaf)
- Semantic similarity
  - node-based
    - Resnik et al.
    - Lin et al.
  - edge-based
    - Pekar et al.
  - Wang et al.
- Semantic similarity between two term sets
  - max
  - avg
  - Best-Match Average (BMA)


API Documentation
------------------------

https://pygosemsim.readthedocs.io/



License
-------------

[MIT license](http://opensource.org/licenses/MIT)



Copyright
--------------

(C) 2018 Seiji Matsuoka
