#!/usr/bin/env python3

import argparse
import json
import os
import pygame
import sys


TILE_IMAGES = '../terrain/terrain.png'


# load and convert tiled maps
# this is a command line utility


def loadMapData(map_file):
    # check 1: the file exists, 2: We can load it, 3: It parses fine
    if not os.path.isfile(map_file):
        print('{0} is not a file'.format(map_file))
        sys.exit(False)
    try:
        map_handle = open(map_file, 'r')
    except IOError:
        print('Could not open file {0}'.format(map_file))
        sys.exit(False)
    # load the data and parse it
    try:
        map_data = json.load(map_handle)
    except Exception as e:
        print('Could not load {0}: {1}'.format(map_file, e))
        sys.exit(False)
    return map_data


def renderMap(map_file):
    map_data = loadMapData(map_file)
    # now we need to load associated bitmap to render
    tile_images = pygame.image.load(TILE_IMAGES)
    # find the individual layers in the json data
    if 'layers' not in map_data:
        print('Error: There are no layers to render in {0}!'.format(map_file))
        sys.exit(False)
    for layer in map_data['layers']:
        print(layer['name'])
    # render each to a surface
    # merge the surfaces
    # save this file


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
        renderMap(options.render)
    elif options.info:
        showMapInfo()

    if len(sys.argv) == 1:
        # no arguments were passes
        parser.print_help()
