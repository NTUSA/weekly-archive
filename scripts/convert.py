#!/usr/bin/env python
import re
import sys

from html import unescape

if len(sys.argv) < 2:
    print('Usage: ./convert.py [issue_id]')
    sys.exit(-1)

with open('issue/{}/index.html'.format(sys.argv[1]), 'r') as f:
    for line in f:
        match = re.match(r'<h3 style[^>]+>(.+)</h3>', line)
        if match:
            print('\n---')
            print(match.group(1))
            continue

        match = re.match(r'<img class="aritcle_cover" src="([^"]+)"', line)
        if match:
            print(unescape(match.group(1)))
            continue

        match = re.match(r'<p style=[^>]+>(.+)</p>', line)
        if match:
            print(match.group(1))
            continue

        match = re.match(r'<span class="author_name">(.+)</span>', line)
        if match:
            print(match.group(1))
            continue

        match = re.match(r'<a target="_blank" href="([^"]+)"', line)
        if match:
            print(unescape(match.group(1)))
            continue
