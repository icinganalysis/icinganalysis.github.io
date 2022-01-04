AUTHOR = 'Donald Cook'
SITENAME = "Blast from the Past:  NACA Icing Publications"
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
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

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
    ('Diversions', '/pages/diversions.html'),
    ('About', '/pages/about.html'),
)
THEME_TEMPLATES_OVERRIDES = ['/home/theepdinker/PycharmProjects/icingblog/notmyidea/templates']
