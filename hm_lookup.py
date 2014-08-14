#!/usr/bin/python3

# Lookup a hash in the MongoDB database

# Copyright 2014 Commons Machinery http://commonsmachinery.se/
# Distributed under an MIT license, please see LICENSE in the top dir.

import pymongo
import base64

import hmsearch

def main(args):
    client = pymongo.MongoClient(args.url)
    db = client[args.name]

    coll_name = hmsearch.collection_name(args)
    coll = db[coll_name]

    q = bytes.fromhex(args.query)

    if len(q) * 8 != args.hash_size:
        exit('invalid hash: {0!r}'.format(args.query))

    print('Searching in {0} for {1}'.format(coll_name, args.query))

    partition = hmsearch.partitioner(args)

    cand = get_candidates(coll, partition, q)

    # Look for matches
    for h, errs in iter(cand.items()):
        if valid_candidate(errs, args):
            distance = hamming_distance(q, h)
            if distance <= args.max_error:
                print(base64.b16encode(h), distance)


def get_candidates(coll, partition, q):
    # Find list of candidates by 1-var-querying the partitions
    cand = {}
    for i, p, bits in partition(q):
        part_name = 'part{0}'.format(i)
        for d in coll.find({part_name: p}, [part_name, 'hash']):

            h = d['hash']
            try:
                errs = cand[h]
            except KeyError:
                errs = cand[h] = []

            if d[part_name][0] == p:
                # exact match
                errs.append(0)
            else:
                # 1-match
                errs.append(1)

    return cand


def valid_candidate(errs, args):
    if args.max_error & 1:
        # odd k
        if len(errs) < 3:
            if len(errs) == 1 or (errs[0] and errs[1]):
                return False
    else:
        # even k
        if len(errs) < 2:
            if errs[0]:
                return False

    return True

def hamming_distance(q, h):
    assert len(q) == len(h)

    distance = 0
    for i in range(len(q)):
        diff = q[i] ^ h[i]
        distance += one_bits[diff]

    return distance


# generate lookup table for number of 1 bits in all byte values
one_bits = [bin(_i).count('1') for _i in range(0, 256)]


if __name__ == '__main__':
    parser = hmsearch.argparser('search for a hash')
    parser.add_argument('query', help='query hash (as hex)')
    main(parser.parse_args())
