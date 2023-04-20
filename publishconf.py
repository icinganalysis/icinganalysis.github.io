# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = ''
# SITEURL = 'https://icinganalysis.github.io'
RELATIVE_URLS = False
#MENUITEMS = (
#    ('Home', SITEURL + '/index.html'),
#    ('Cylinders', SITEURL + '/icing-on-cylinders.html'),
#    ('Thermodynamics', '/icing-thermodynamics.html'),
#    ('Ice Shapes', '/ice-shapes-and-their-effects.html'),
#    ('Diversions', SITEURL + '/diversions.html'),
#    ('Evaporation', SITEURL + '/water-drop-evaporation.html'),
#    ('Icing Tunnels', SITEURL + '/icing-wind-tunnel-test-thread.html'),
#    ('Instruments', SITEURL + '/meteorological-instruments.html'),
#    ('Ice Protection', SITEURL + '/ice-protection.html'),
#    ('About', SITEURL + '/about.html'),
#)
MENUITEMS = (
    ('Home', '/index.html'),
    ('Cylinders', '/icing-on-cylinders.html'),
    ('Thermodynamics', '/icing-thermodynamics.html'),
    ('Ice Shapes', '/ice-shapes-and-their-effects.html'),
    ('Diversions', '/diversions.html'),
    ('Evaporation', '/water-drop-evaporation.html'),
    ('Icing Tunnels', '/icing-wind-tunnel-test-thread.html'),
    ('Instruments', '/meteorological-instruments.html'),
    ('Ice Protection', '/ice-protection.html'),
    ('Meteorology', '/meteorology-of-icing-clouds.html'),
    ('About', '/about.html'),
)

FEED_ALL_ATOM = ''
CATEGORY_FEED_ATOM = ''


DELETE_OUTPUT_DIRECTORY = False

#DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

