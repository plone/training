#! /usr/bin/python

import yaml
import pprint
import sys

pprint.pprint(yaml.load(sys.stdin.read()), indent=2)
