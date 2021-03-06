#!/usr/bin/env bash

cd ~/ActiveData
export PYTHONPATH=.

# usage: gunicorn [OPTIONS] [APP_MODULE]
#
# [APP_MODULE] IS A POORLY DOCUMENTED MINI-LANGUAGE:
#
# <APP_MODULE> = <MODULE_PATH> ":" <FLASK_OBJECT>
# <APP_MODULE> = <MODULE_PATH> ":" <METHOD_CALL>
#
# where
#
# <MODULE_PATH> = is a dot delimited path to the module
# <METHOD_CALL> = ?Python syntax? method call that will return a Flask object
# <FLASK_OBJECT> = the actual flask object in module (do not called `run()`)

/usr/local/bin/gunicorn --pythonpath . --config resources/config/gunicorn.py 'active_data.app:setup(settings="resources/config/staging_settings.json")'
