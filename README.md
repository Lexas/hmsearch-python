hmsearch-python
===============

*NOTE: this implementation will be dropped, and replaced by a Python
API to the C++ library https://github.com/commonsmachinery/hmsearch
instead.*

Old info
========

This is an implementation of the hamming distance algorithm HmSearch
using MongoDB for storing the hashes and indices.

Usage
-----

These tools require Python 3.

All scripts obey `--help`.

`hm_initdb.py` creates the necessary MongoDB indices.

`hm_insert.py` inserts hashes (as hex strings) read from stdin into
the database.

`hm_lookup.py` finds matches for a hash in the database with a maximum
hamming distance.



Limitations
-----------

The code only supports a binary value space (i.e. 0 and 1), not the
larger spaces of full HmSearch.

Hashes must be an even number of bytes.

As it's currently mainly intended to explore how well the algorithm
performs, the bulk of the code are implemented directly in scripts
rather than as in a Python module.  This should be fixed.

The partitioning should be more efficient too, rather than
quick-and-dirty manipulation of numbers as binary strings.

Long-term it could be interesting with other backends than
MongoDB.


License
-------

Copyright 2014 Commons Machinery http://commonsmachinery.se/

Distributed under an MIT license, please see LICENSE in the top dir.

Contact: dev@commonsmachinery.se

