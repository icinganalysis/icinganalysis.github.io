AUTHOR = 'Donald Cook'
SITENAME = "Blast from the Past: NACA Icing Publications"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/icinganalysis/icinganalysis.github.io'),
#          ('twitter', 'https://twitter.com/icinganalysis'),
          ('linkedin', 'https://www.linkedin.com/in/donald-cook-96204316a/'),
          ('email', 'mailto:icinganalysis@gmail.com'),
          ('mastodon', 'https://historians.social/@icinganalysis'),
          )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

DEFAULT_DATE = 'fs'
# THEME = 'aboutwilson'
# THEME = 'pelicanyan-master'
LOAD_CONTENT_CACHE = False

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
SUMMARY_MAX_LENGTH = 40

# DIRECT_TEMPLATES = ['blog', 'index']
# PAGINATED_TEMPLATES = ['blog']
INDEX_SAVE_AS = 'blog.html'
MENUITEMS = (
    ('Home', '/'),
    ('Cylinders', '/icing-on-cylinders.html'),
    ('Thermodynamics', '/icing-thermodynamics.html'),
    ('Ice Shapes', '/ice-shapes-and-their-effects.html'),
    ('Diversions', '/diversions.html'),
    ('Instruments', SITEURL + '/meteorological-instruments.html'),
    ('About', '/about.html'),
)
THEME_TEMPLATES_OVERRIDES = ['/home/theepdinker/PycharmProjects/icinganalysis.github.io/notmyidea/templates']
DELETE_OUTPUT_DIRECTORY = False
