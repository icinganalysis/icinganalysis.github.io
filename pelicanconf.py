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
          ('email', 'mailto:icinganalysis@proton.me'),
          ('mastodon', 'https://historians.social/@icinganalysis'),
          )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

DEFAULT_DATE = 'fs'
# THEME = 'aboutwilson'
# THEME = 'pelicanyan-master'
LOAD_CONTENT_CACHE = False


CHECK_MODIFIED_METHOD = 'mtime'
CACHE_CONTENT = True


DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
SUMMARY_MAX_LENGTH = 150

# DIRECT_TEMPLATES = ['blog', 'index']
# PAGINATED_TEMPLATES = ['blog']
INDEX_SAVE_AS = 'blog.html'
MENUITEMS = (
    ('Home', '/index.html'),
    ('Suggested Reading Order', '/site-navigation-and-suggested-reading-order.html'),
    ('Latest Posts', '/archives.html'),
    ('About', '/about.html'),
)
THEME_TEMPLATES_OVERRIDES = ['/home/theepdinker/PycharmProjects/icinganalysis.github.io/notmyidea/templates']
DELETE_OUTPUT_DIRECTORY = False

STATIC_PATHS = [
    # 'images',
    'extra',  # this
]
EXTRA_PATH_METADATA = {
    # 'extra/custom.css': {'path': 'custom.css'},
    # 'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},  # and this
    # 'extra/CNAME': {'path': 'CNAME'},
    # 'extra/LICENSE': {'path': 'LICENSE'},
    # 'extra/README': {'path': 'README'},
}


