#!/usr/bin/env python3

import argparse
import json
import os
import pygame
import sys
import xml.etree.ElementTree as ET


TILE_IMAGES = '../terrain/terrain.png'
XML_TILES = '../terrain/Terrain.tsx'


# load and convert tiled maps
# this is a command line utility

def loadXMLTiles():
    # parse the tile xml and return an index:rect dict
    tiles = {}
    tree = ET.parse(XML_TILES)
    root = tree.getroot()
    # get every tile
    for tile in root.iter('tile'):
        print(tile.attrib['id'])
        print(tile.attrib['terrain'])


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
        print('Error: There are no layers to render!')
        sys.exit(False)
    layers = map_data['layers']
    # make sure they all have data
    for i in layers:
        for j in ['data', 'width', 'height', 'name']:
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


def saveRenderedLayer(final_surface, map_file):
    # change the file extension to png
    new_filename = '{0}{1}'.format(os.path.splitext(map_file)[0], '.png')
    # save the rendered surface
    pygame.image.save(final_surface, new_filename)


def renderMap(map_file):
    map_data = loadMapData(map_file)
    # now we need to load associated bitmap to render
    tile_images = pygame.image.load(TILE_IMAGES)
    # find the individual layers in the json data

    layers = getMapLayers(map_data)
    map_size = getSize(map_data)
    render_layers = []
    for layer in layers:
        # render each to a surface
        try:
            length = layer['width'] * layer['height']
            data = layer['data']
        except KeyError as e:
            print('Map data is missing elements: {0}'.format(e))
            sys.exit(0)
        render_surface = pygame.Surface((map_size.width, map_size.height))
        if len(data) != length:
            print('Error: data length different from map size in layer {0}.'.format('name'))
            sys.exit(0)
        for tile_value in data:
            # find this tile
            # blit it with full alpha
            pass
        render_layers.append(render_surface)
    # render layers 1, 2 etc onto layer 0
    for layer in render_layers[1:]:
        render_layers[0].blit(layer, (0, 0))
    # save the rendered layer
    saveRenderedLayer(render_layers[0], map_file)


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

    loadXMLTiles()
