from blueprints import app, manager, jwt
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from logging.handlers import RotatingFileHandler
import logging, sys
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

# ===INITIATE FLASK-RESTFUL INSTANCE=== #
api = Api(app, catch_all_404s=True)

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'db':
            manager.run()
            sys.exit()
    except Exception as e:
        # define log format and create a rotating log with max size and max backup to 10 files
        logging.getLogger().setLevel('INFO')
        formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" %(app.root_path, '../storage/log/app.log'),maxBytes=1000000, backupCount=10)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

        app.run(debug=False, host='0.0.0.0', port =5000)