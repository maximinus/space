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


def getMapLayers(map_data):
    if 'layers' not in map_data:
        print('Error: There are no layers to render in {0}!'.format(map_file))
        sys.exit(False)
    layers = map_data['layers']
    # make sure they all have data
    required = ['data', 'width', 'height', 'name']
    for i in layers:
        for j in layers:
            if j not in i:
                print('Error: Missing layer info {0} in layer'.format(j))
                sys.exit(False)
    return layers


class ItemSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def size(self):
        return self.x * self.y


def getSize(data):
    # data could be a layer or the map
    try:
        width = data['width']
        height = data['height']
    except KeyError as e:
        print('Error: Missing data in map data: {0}'.format(e))
        sys.exit(False)
    return ItemSize(width, height)


def renderMap(map_file):
    map_data = loadMapData(map_file)
    # now we need to load associated bitmap to render
    #tile_images = pygame.image.load(TILE_IMAGES)
    # find the individual layers in the json data

    layers = getMapLayers(map_data)
    map_size = getMapSize(map_data)
    render_layers = []
    for layer in layers:
        # render each to a surface
        try:
            length = layer['width'] * layer['height']
            data = layer['data']
            name = layer['name']
        except KeyError as e:
            print('Map data is missing elements: {0}'.format(e))
            sys.exit(0)
        render_surface = pygame.Surface((xsize, ysize))
        if len(data) != length:
            print('Error: data length different from map size in layer {0}.'.format('name'))
            sys.exit(0)
        for tile_value in data:
            # find this tile
            # blit it with full alpha


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
