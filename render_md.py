#!/bin/env python

"""
render_md.py
------------

A simple markdown renderer, it supports adding a style sheets using CDN urls

Relative urls should also work. (but be aware... you will need to handle these yourself!)

Usage:
  python render_md.py -f 'in_file.md' -o 'out_file.html' [-u style_url]

Required Arguments:
  -f --file       The *.md file to be parsed
  -o --output     The output file path for the rendered HTML

Optional Arguments:
  -h --help       Show usage (eg. print this...)
  -u --style-url  The url of a CSS sheet to be included in template

"""

import sys
import os

import markdown
import getopt
from jinja2 import Template


# html template
html_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{{ title }}</title>
    {% if style_url %}
      <link rel="stylesheet" type="text/css" media="all" href="{{ style_url }}"/>
    {% endif %}
  </head>
  <body>
    {{ content }}
  </body>
</html>
"""


def get_options():
    '''get_options: gets the args passed in from cli'''
    # getopts definitions
    option_args = 'hf:u:o:'
    option_args_extended = ['help', 'file=', 'style-url=', 'output=']    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   option_args, 
                                   option_args_extended)
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        exit(2)
    in_file = None
    out_file = None
    style_url = None
    for o, a in opts:
        if o in ("-h", "--help"):
            exit()
        elif o in ("-o", "--output"):
            out_file = a
        elif o in ("-f", "--file"):
            in_file = a
        elif o in ("-u", "--style-url"):
            style_url = a
        else:
            assert False, "unhandled option"
    config = {'in_file': in_file, 
              'out_file': out_file, 
              'style_url': style_url}
    return config


def render(text, config):
    """
render
------

Parses and inserts the markdown text into a basic html template.
Adds a style link to template header if included

text: The markdown formatted content to be parsed and inserted into the html document

config: The config dictionary that houses the style_url
    """
    template = Template(html_template)
    content = markdown.markdown(text, ['markdown.extensions.extra', 'markdown.extensions.toc'])
    html = template.render({'content': content, 'style_url': config['style_url']})
    return html


def usage():
    print(__doc__)


def exit(exit_code=0):
    usage()
    sys.exit(exit_code)


if __name__ == "__main__":
    # load config from cli
    config = get_options()
    
    # check the mandatory args
    if config['out_file'] == None:
        print("No out_file specified!")
        exit(2)
    elif config['in_file'] == None:
        print("No in_file specified!")
        exit(2)
    
    # make sure input file exists
    if not os.path.exists(config['in_file']):
        usage()
        sys.exit("Input file cannot be found!")
    
    # render html from markdown
    with open(config['in_file'], "r") as f:
        text = f.read()    
    html = render(text, config)
    
    # output html file
    with open(config['out_file'], "w") as f:
        f.write(html)
