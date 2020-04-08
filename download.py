#!/usr/bin/python

'''
Fetches, unzips & reorgs the repos.
'''

import json

st = os.stat()

with open('manifest.json', 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)

