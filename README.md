# render_md

A simple markdown renderer, it supports adding a style sheets using CDN urls

Relative urls should also work. (but be aware... you will need to handle these yourself! eg. make sure you put them in the right spot relative to the final html document.)

Usage:
  python render_md.py -f 'in_file.md' -o 'out_file.html' [-u style_url]

Required Arguments:
  -f --file       The *.md file to be parsed
  -o --output     The output file path for the rendered HTML

Optional Arguments:
  -h --help       Show usage (eg. print this...)
  -u --style-url  The url of a CSS sheet to be included in template
  
