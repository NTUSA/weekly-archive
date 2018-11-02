#!/usr/bin/env python
import re
from html import unescape

output = open('data.py', 'w+')
output.write("""
from issues.models import *

data = [""")

for issue in range(113, 132):
    output.write('\n    # {}\n'.format(issue))
    with open('issue/{}/index.html'.format(issue), 'r') as f:
        name, content, provider, url = '', '', '', ''
        column = 0
        for line in f:

            if '<div class="footer"' in line:
                break

            match = re.search(r'<h3 style[^>]+>(.+)</h3>', line)
            if match:
                if name:
                    output.write("    ({}, '{}', '{}', '{}', {}, '{}'),\n".format(issue, name, content, provider, column, url))
                name, content, provider, url = unescape(match.group(1)), '', '', ''
                continue

            match = re.search(r'<p style=[^>]+>([^<]+)</p>', line, flags=re.DOTALL)
            if match:
                content = unescape(match.group(1))
                continue

            match = re.search(r'<span class="author_name">([^<]+)', line)
            if match:
                provider = match.group(1)
                continue

            match = re.search(r'<a target="_blank" href="([^"]+)"', line)
            if match:
                url = unescape(match.group(1))
                continue

            if '<div class="box_title"' in line:
                column += 1

        if name:
            output.write("    ({}, '{}', '{}', '{}', {}, '{}'),\n".format(issue, name, content, provider, column, url))

output.write("""]

issues = { i.id: i for i in Issue.objects.all() }
columns = { i.id : i for i in Column.objects.all() }
providers = { i.name: i for i in Provider.objects.all() }

for issue_id, name, content, provider, column, url in data:
    article = Article(issue=issues[issue_id], name=name, content=content,
                      provider=providers.get(provider),
                      column=columns[column],
                      url=url)
    article.save()
    print(article)

""")
output.close()
