class Config(object):
    TESTING = False
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    def __init__(self):
        self.BROKER_URL = 'redis://172.18.0.2:6379/0'
        self.CELERY_RESULT_BACKEND = 'redis://172.18.0.2:6379/0'
        self.SQL_HOST = '172.18.0.3'
        self.SQL_PORT = 5432
        self.SQL_USER = 'root'
        self.SQL_PASS = 'password'
        self.ZIPCODE_API = 'https://www.zipcodeapi.com/rest/'
        self.ZIP_API_TOKEN = 'DemoOnly00Vjbv48XeZWzzxdp61OmV0oaOKqce7Ev2zZWZTDUxNuJbrUPObfCtQ7'


class TestingConfig(Config):
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    BROKER_URL = ''
    CELERY_RESULT_BACKEND = ''
    SQL_HOST = ''
    SQL_PORT = ''
    SQL_USER = ''
    SQL_PASS = ''
