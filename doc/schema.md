Database schema
---------------

Each hash is stored in a document (which could potentially include
additional data about the hash).

    {
        hash: binary,    # full hash
        part0: [ int ]   # list of partition followed by its 1-variants
        part1: [ int ]
        ...
        partN: [ int ]
    }

The hash field is indexed to allow exact searches, and the values in
the partitions are all indexed with multi-key indices.


Collections
-----------

To identify the setup of the database, the hash size `N` and maximum
error `k` is included in the collection name:

    hash_N_k
