# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
# SITEURL = ''
SITEURL = 'https://icinganalysis.github.io'
RELATIVE_URLS = False
MENUITEMS = (
    ('Home', SITEURL + '/index.html'),
    ('Cylinders', SITEURL + '/icing-on-cylinders.html'),
    ('Thermodynamics', '/icing-thermodynamics.html'),
    ('Ice Shapes', '/ice-shape-and-their-effects.html'),
    ('Diversions', SITEURL + '/diversions.html'),
    ('Evaporation', SITEURL + '/water-drop-evaporation.html'),
    ('About', SITEURL + '/about.html'),
)

FEED_ALL_ATOM = ''
CATEGORY_FEED_ATOM = ''


DELETE_OUTPUT_DIRECTORY = False

#DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

