#!/usr/bin/env python
''' Takes an IMPOSM shape file for streets and identifies streets by type (according to last word in name. Outputs to new file

Streets with no name are removed from the output

Street map files obtained from https://mapzen.com/metro-extracts/

Usage: label_street_type.py <input_path> <output_path>

Code based off of https://gist.github.com/vlandham/7051466
'''
__author__ = 'julenka'

import sys
import fiona.collection as collection
from collections import Counter

in_path = sys.argv[1]
out_path = sys.argv[2]

all_street_types = Counter()
with collection(in_path, "r") as input:
    schema = input.schema.copy()
    meta = input.meta.copy()
    meta['schema']['properties']['road_type'] = 'str:32'
    with collection(out_path, 'w', **meta) as output:
        for feature in input:
            feature_copy = feature.copy()
            street_name = feature['properties']['name']
            if street_name is None:
                continue
            street_type = street_name.strip().split(' ')[-1]
            # Need to special case this one
            if street_name == "Boulevard of the Allies":
                street_type = "Boulevard"
            feature_copy['properties']['road_type'] = street_type
            all_street_types[street_type] += 1
            output.write(feature_copy)

# as a bonus, uncomment to print out all street types for later reference
# for k,v in all_street_types.items():
#     print '{}, {}'.format(k,v)
