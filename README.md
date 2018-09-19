
pygosemsim
===================================================

**pygosemsim** is a GO (Gene Ontology) semantic similarity calculation library for Python.



Getting started
------------------


### Install


### Download GO datasets and build GO graph

```
>>> from pygosemsim import download
>>> download.obo("go-basic")
Download started: http://purl.obolibrary.org/obo/go/go-basic.obo
Downloaded 32.2MB of 32.2MB (100.0 %)
Download finished: go-basic.obo (32.2) MB

>>> from pygosemsim import graph
>>> import networkx as nx
>>> G = graph.from_resource("go-basic")
format-version: 1.2, data-version: releases/2018-09-17

>>> nx.ancestors(G, "GO:0004396")
{'GO:0003674', 'GO:0003824', 'GO:0016301', 'GO:0016740', 'GO:0016772', 'GO:0016773', 'GO:0019200'}

>>> nx.descendants(G, "GO:0004396")
{'GO:0004340', 'GO:0008865', 'GO:0019158'}
```


### GO term semantic similarity

```
>>> from pygosemsim import similarity
>>> similarity.resnik(G, "GO:0004340", "GO:0019158")
13.459
>>> similarity.wang(G, "GO:0004340", "GO:0019158")
0.804
```


### Download and parse gene annotation file

```
>>> download.gaf("goa_human")
Download started: http://geneontology.org/gene-associations/goa_human.gaf.gz
Downloaded 7.9MB of 7.9MB (100.0 %)
Download finished: goa_human.gaf.gz (7.9) MB

>>> from pygosemsim import annotation
>>> annot = annotation.from_resource("goa_human")
gaf-version: 2.1

>>> len(annot)
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

```
>>> import functools
>>> from pygosemsim import term_set

>>> def sim_func(term1, term2):
>>>     try:
>>>         sim = similarity.resnik(G, term1, term2)
>>>     except ValueError:
>>>         sim = 0
>>>     return sim

>>> trpv1 = annot["Q8NER1"]["annotation"].keys()
>>> trpa1 = annot["O75762"]["annotation"].keys()
>>> term_set.sim_bma(trpv1, trpa1, sim_func)

```


Features
----------

- File parsers (.obo, .gaf)
- Semantic similarity
  - Resnik method
  - Lin method
  - Wang method
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
