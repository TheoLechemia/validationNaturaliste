import os, sys

# Activate your virtual env
activate_env=os.path.expanduser(os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))


APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIR)

from werkzeug.debug import DebuggedApplication

from Apps.initApp import app as application

jinja_options = application.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='{%',
    block_end_string='%}',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
))
application.jinja_options = jinja_options








from flask.ext.compress import Compress
compress = Compress()
compress.init_app(application)




from Apps.validation.validationViews import validation


application.register_blueprint(validation, url_prefix='/validation')




