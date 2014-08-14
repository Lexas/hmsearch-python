#!/usr/bin/python3

# Initialise the indices in a MongoDB collection for looking up hashes

# Copyright 2014 Commons Machinery http://commonsmachinery.se/
# Distributed under an MIT license, please see LICENSE in the top dir.

import pymongo

import hmsearch

def main(args):
    client = pymongo.MongoClient(args.url)
    db = client[args.name]

    coll_name = hmsearch.collection_name(args)
    part_count = hmsearch.partitions(args)

    sys.stdout.write('Creating {0} with {1} partitions\n'.format(coll_name, part_count))

    coll = db[coll_name]
    coll.create_index([('hash', pymongo.ASCENDING)])
    for i in range(part_count):
        coll.create_index([('part{0}'.format(i), pymongo.ASCENDING)])


if __name__ == '__main__':
    parser = hmsearch.argparser('create mongodb indices for hmsearch')
    main(parser.parse_args())
