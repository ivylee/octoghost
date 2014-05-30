#!/usr/bin/env python

from bs4 import BeautifulSoup
import arrow
import pypandoc
import codecs

posts_dir = "OCTOPRESS_HOME/source/_posts/"
blog_dir = "PUBLISHED_HOME/blog/"
post_html_list = "ALL_PUBLISHED_HTML_ABSOLUTE_PATH_LIST_FILE" # easily generated from command line

def create_markdown(input_html_file, posts_dir, markdown_file_title):

    with open(input_html_file, 'r') as in_html:
        html = unicode(in_html.read(), "utf-8")

    soup = BeautifulSoup(html)
    title_string = soup.select(".entry-title")[0].contents[0]
    date_time = soup.time['datetime']
    date_string = unicode(arrow.get(date_time).format('YYYY-MM-DD HH:mm:ss'))
    markdown_file_date_string = arrow.get(date_time).format('YYYY-MM-DD')
    tags = soup.select(".category")[0].contents
    tags_string = ",".join(tags)
    post_content = soup.select(".entry-content")[0]
    markdown_content = pypandoc.convert(post_content.prettify(), "md", format = "html")

    out_markdown = codecs.open(posts_dir + markdown_file_date_string + '-' +
            markdown_file_title + '.markdown', 'w', 'utf-8')
    out_markdown.write('---\n')
    out_markdown.write('layout: post\n')
    out_markdown.write('title: "%s"\n' % title_string)
    out_markdown.write('date: %s\n' % date_string)
    out_markdown.write('comments: true\n')
    out_markdown.write('categories: %s\n' % tags_string)
    out_markdown.write('---\n')
    out_markdown.write(markdown_content)
    out_markdown.close()

with open(blog_dir + post_html_list, 'r') as posts_html_file:
    n = 0
    for post_html in posts_html_file:
        n = n + 1
        print("reading file %d" % n)
        markdown_file_title = post_html.split('/')[10]
        create_markdown(post_html.strip(), posts_dir, markdown_file_title)
