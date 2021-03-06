AUTHOR = 'Phil Nicholls'
SITENAME = 'Phil Nicholls'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Jerusalem'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

ARTICLE_PATHS = ['portfolio']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/philjnicholls'

PHOTO_LIBRARY = '~/projects/philjnicholls.github.io/content/images'
PHOTO_ARTICLE = (667, 500, 80)
PHOTO_SQUARE_THUMB = True
