#!/usr/bin/env python3

import sys
import argparse

# load and convert tiled maps
# this is a command line utility, options:

# convert_tiled.py --render new_file.png
# or
# convert_tiled.py -r new_file.png


def renderMap():
    print('Rendering')


def showMapInfo():
    print('Map info')


def setParseOptions():
    parser = argparse.ArgumentParser(description='Converter for Tiled json maps')

    render_help = 'Render the given map to a single image'
    parser.add_argument('-r', '--render', metavar='map', help=render_help)
    info_help = 'Show map statistics'
    parser.add_argument('-i', '--info', metavar='map', help=info_help)

    return parser


if __name__ == '__main__':
    parser = setParseOptions()
    options = parser.parse_args()

    if options.render:
        # render the given map
        renderMap()
    elif options.info:
        showMapInfo()

    if len(sys.argv) == 1:
        # no arguments were passes
        parser.print_help()
