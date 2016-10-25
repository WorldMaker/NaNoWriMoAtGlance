# NaNoWriMoAtGlance
# Copyright (C) 2013 Max Battcher. Some Rights Reserved. Licensed for use under the Ms-RL.
from django.shortcuts import redirect, render

NOTIFICATION_TYPES = {
                      'p': {'name': 'Profile', 'has_source': True},
                      'r': {'name': 'Region', 'has_source': True},
                      's': {'name': 'Site Statistics', 'has_source': False},
                      'g': {'name': 'Daily Goal', 'has_source': False},
                      'x': {'name': 'None', 'has_source': False},
                     }

def index(request):
    """
    Index view for NaNoWriMoAtGlance
    """
    tile1type, tile1source = request.GET['tile1type'], request.GET['tile1source']
    tile2type, tile2source = request.GET['tile2type'], request.GET['tile2source']
    if tile1type == 'x' and tile2type != 'x':
        tile1type, tile1source, tile2type = tile2type, tile2source, 'x'
    tile3type, tile3source = request.GET['tile3type'], request.GET['tile3source']
    if tile2type == 'x' and tile3type != 'x':
        tile2type, tile2source, tile3type = tile3type, tile3source, 'x'
    if tile1type == 'x' and tile2type == 'x' and tile3type == 'x':
        return redirect('/')
    if tile1type not in NOTIFICATION_TYPES or tile2type not in NOTIFICATION_TYPES or tile3type not in NOTIFICATION_TYPES:
        return redirect('/')
    tile1uri, tile2uri, tile3uri = None, None, None
    tile1uri = request.build_absolute_uri(not NOTIFICATION_TYPES[tile1type]['has_source'] and '/notification/%s' % tile1type or '/notification/%s/%s' % (tile1type, tile1source))
    if tile2type != 'x':
        tile2uri = request.build_absolute_uri(not NOTIFICATION_TYPES[tile2type]['has_source'] and '/notification/%s' % tile2type or '/notification/%s/%s' % (tile2type, tile2source))
    if tile3type != 'x':
        tile3uri = request.build_absolute_uri(not NOTIFICATION_TYPES[tile3type]['has_source'] and '/notification/%s' % tile3type or '/notification/%s/%s' % (tile3type, tile3source))
    return render(request, 'livetiles/index.html', {
                                                    'tile1': NOTIFICATION_TYPES[tile1type], 
                                                    'tile1source': tile1source,
                                                    'tile1uri': tile1uri,
                                                    'tile2': NOTIFICATION_TYPES[tile2type],
                                                    'tile2source': tile2source,
                                                    'tile2uri': tile2uri,
                                                    'tile3': NOTIFICATION_TYPES[tile3type],
                                                    'tile3source': tile3source,
                                                    'tile3uri': tile3uri,
                                                   })

def context_p(source):
    """
    Template context for Profile
    """
    import requests
    import xml.etree.cElementTree as ET
    r = requests.get('http://nanowrimo.org/wordcount_api/wc/%s' % source)
    tree = ET.fromstring(r.text)
    return dict((c.tag, c.text) for c in tree.getchildren())

def context_r(source):
    """
    Template context for Region
    """
    import requests
    import xml.etree.cElementTree as ET
    r = requests.get('http://nanowrimo.org/wordcount_api/wcregion/%s' % source)
    tree = ET.fromstring(r.text)
    return dict((c.tag, c.text) for c in tree.getchildren())

def context_s(source):
    """
    Template context for Site Stats
    """
    import requests
    import xml.etree.cElementTree as ET
    r = requests.get('http://nanowrimo.org/wordcount_api/wcstatssummary')
    tree = ET.fromstring(r.text)
    return dict((c.tag, c.text) for c in tree.getchildren())

def context_g(source):
    """
    Template context for Daily Goal
    """
    import datetime
    import math
    today = datetime.datetime.today()
    if today.month != 11:
        return { 'daynumber': 0, 'words': 0, }
    return { 'daynumber': today.day, 'words': int(math.ceil(50000 / 30.0 * today.day)), }

CONTEXT_GENERATOR = {
                     'p': context_p,
                     'r': context_r,
                     's': context_s,
                     'g': context_g,
                    }

def notification(request, type, source):
    """
    Notification xml for a tile
    """
    return render(request, 'livetiles/tile_%s.xml' % type, CONTEXT_GENERATOR[type](source),
                  content_type='text/xml')