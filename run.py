import os

from werkzeug.utils import import_string

from app.dependencies_container import create_context

os.environ['APP_SETTINGS'] = 'app.config.config.DevelopmentConfig'
app_settings = os.getenv("APP_SETTINGS")
cfg = import_string(app_settings)()
config = vars(cfg)

context, app, celery = create_context(config)

from app.events import related_zip_data
from app.view import *


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5004, debug=True)
