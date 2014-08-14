#!/usr/bin/python

# Insert a hash into the MongoDB database

# Copyright 2014 Commons Machinery http://commonsmachinery.se/
# Distributed under an MIT license, please see LICENSE in the top dir.

import pymongo
import math

import hmsearch

def main(args):
    client = pymongo.MongoClient(args.url)
    db = client[args.name]

    coll_name = hmsearch.collection_name(args)
    coll = db[coll_name]

    print('Indexing into {0}'.format(coll_name))

    partition = hmsearch.partitioner(args)

    for line in sys.stdin:
        line = line.strip()
        h = bytes.fromhex(line)

        if len(h) * 8 != args.hash_size:
            sys.stderr.write('invalid hash: {0!r}\n'.format(line))
            continue

        d = { 'hash': h }

        for i, p, bits in partition(h):
            variants = [p]

            # Flip each bit in the partition
            for j in range(bits):
                variants.append(p ^ (1 << j))

            d['part{0}'.format(i)] = variants

        coll.insert(d)


if __name__ == '__main__':
    parser = hmsearch.argparser('insert hex hashes from stdin into db')
    main(parser.parse_args())
