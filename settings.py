from os import environ

SESSION_CONFIGS = [
    dict(
        name='Main',
        app_sequence=[
            'intro',
            'tg',
             'dg',
            'tg2',
            'outro'
        ],
        num_demo_participants=5
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=1.00, doc=""
)

PARTICIPANT_FIELDS = [
    'northern',
    'return1',
    'return2',
    'return3',
    'tgfirst',
    'dictator',
    'paymentstage'
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4808892522632'
