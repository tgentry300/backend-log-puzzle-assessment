#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse
import shutil

html_template = """
<html>
<head>
</head>
<body>
{}
</body>
</html>
"""


def url_sort_func(url_list):
    """Sorts URLs based on last section of letters"""
    sort_list = re.search(r'(/p-\w+-)(\w*)', url_list)
    return sort_list.group(2)


def create_img_template(path):
    """Create's image template to put into html"""
    return '<img src="{}"/>'.format(path)


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    with open(filename, 'r') as f:

        file_text = f.read()
        match_list = re.findall(r'GET (\S*puzzle\S*)', file_text)

        if re.search(r'(/p-\w+-)(\w*)', file_text):
            new_match_list = sorted(['https://code.google.com'
                                    + url for url in set(match_list)])
            return sorted(new_match_list, key=url_sort_func)
        else:
            return sorted(['https://code.google.com'
                          + url for url in set(match_list)])


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    os.mkdir(dest_dir)

    with open('index.html', 'w') as index:
        img_temp_list = []
        for i, url in enumerate(img_urls):
            urllib.urlretrieve(url, 'img{}'.format(i))
            shutil.move('img{}'.format(i), '{}'.format(dest_dir))
            img_temp_list.append(create_img_template('img{}'.format(i)))

        shutil.move('index.html', dest_dir)
        index.write(html_template.format('\n'.join(img_temp_list)))


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
    # print(read_urls('animal_code.google.com'))
