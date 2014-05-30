#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert all markdown files (octopress style) to JSON (ghost style).

Assuming:
    - Layout in Octopress is 'post'
    - Ignores 'comments' and 'shared' and probably other metadata.

Requires:
    pip install translitcodec

Usage:
    - Access /ghost/debug and export the database
    - Run the script on a directory with the markdown files
        python octopress2ghost.py <octopress-folder> <ghost-data-json> | python -mjson.tool > ready-to-import.json
    - Access /ghost/debug and import the modified file
"""

import sys
import re
import json
import uuid
import datetime
import time
import glob
import codecs
import os

__author__ = "Simone Margaritelli, Julián Romero"
__copyright__ = "Copyright 2014"
__license__ = "GPL"
__version__ = "3.0.0"
__maintainer__ = "Simone Margaritelli"
__email__ = "evilsocket@gmail.com"
__status__ = "Production"

# ghost settings
post_id = 1
author_id = 1
next_tag_id = 1
post_tag_id = 1
lang = "en_US"

# internal
ARG_INPUT_FOLDER = 1
ARG_OUTPUT_JSON = 2

if len(sys.argv) < 3:
    ARG_INPUT_FOLDER = "."
    ARG_OUTPUT_JSON = "output.json"

import translitcodec
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

posts = []
tags = []
posts_tags = []
categories = {}

for markdown_file in glob.glob("%s/*.markdown" % sys.argv[ARG_INPUT_FOLDER]):
    is_metadata = False
    is_post = False
    post = {
            "id":           post_id,
            "uuid":         str(uuid.uuid4()),
            "created_by":   author_id,
            "updated_by":   author_id,
            "published_by": author_id,
            "language":     lang,
            "status":       "published",
            "slug":         os.path.basename(markdown_file).split('.')[0]
            }
    markdown = []
    with codecs.open(markdown_file, "r", "utf-8") as f:
        for line in f:
            line = line.rstrip()
            if line == "---":
                if is_metadata:
                    is_post = True
                else:
                    is_metadata = True
                continue
            if is_post:
                m = re.match(r'\{% img (?P<image>.+) %\}', line)
                if m:
                    markdown.append("![{0}]({0})".format(m.group("image")))
                else:
                    markdown.append(line)
            elif is_metadata:
                if line == "":
                    continue
                for match in re.finditer(r'(?P<field>\w+):\s*(?P<value>.*)', line):
                    field = match.group("field")
                    value = match.group("value")
                    if field == "title":
                        title = re.sub(r'^"|"$', '', value)
                        post["title"] = title
                    elif field == "published":
                        post["status"] = value == "true" and "published" or "draft"
                    elif field == "date":
                        # FIX: This fixes the ValueError when timezone is at the end of the value
                        values = value.split(':')
                        if (len(values) > 1):
                            value = values[0] + ":" + values[1]
                        else:
                            value = values[0] + " " + "00:00"
                       
                        d = datetime.datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")
                        t = int(time.mktime(d.timetuple()) * 1e3)
                        post["created_at"] = t
                        post["updated_at"] = t
                        post["published_at"] = t
                    elif field == "categories":
                        the_tags = value.split(" ")
                        for tag in the_tags:
                            if not categories.has_key(tag):
                                categories[tag] = next_tag_id
                                next_tag_id = next_tag_id + 1
                                tags.append({
                                    "id": categories[tag],
                                    "slug": slugify(tag),
                                    "name": tag,
                                    "uuid": str(uuid.uuid4())
                                    })
                            posts_tags.append({
                                "id": post_tag_id,
                                "post_id": post_id,
                                "tag_id": categories[tag],
                                })
                            post_tag_id = post_tag_id + 1
                    else:
                        pass
            else:
                raise Exception('Unexpected exception!')

    post_id = post_id + 1
    post["markdown"] = "\n".join(markdown)
    posts.append(post)

ghost_json_file_name = sys.argv[ARG_OUTPUT_JSON]
ghost_data = json.loads(open(ghost_json_file_name).read())

ghost_data['data']['posts'] = posts
ghost_data['data']['tags'] = tags
ghost_data['data']['posts_tags'] = posts_tags

print json.dumps(ghost_data)

