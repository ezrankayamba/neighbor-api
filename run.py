# run.py


import os

from app import create_app

# config_name = os.getenv('FLASK_CONFIG')
config_name = 'dev'
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
