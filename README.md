
pygosemsim
===================================================

**pygosemsim** is a GO (Gene Ontology) semantic similarity calculation library for Python.



Getting started
------------------


### install


### download datasets


### build GO graph

```
from pygosemsim import graph, parser, similarity

G = parser.obo_to_graph("/path/to/go_basic.obo")
annot = parser.annotation("/path/to/human.goa")
G.set_annotations(annot)

sim = similarity.resnik(G, term1, term2)

print(sim)

```


Features
----------





API Documentation
------------------------

https://pygosemsim.readthedocs.io/



License
-------------

[MIT license](http://opensource.org/licenses/MIT)



Copyright
--------------

(C) 2018 Seiji Matsuoka
