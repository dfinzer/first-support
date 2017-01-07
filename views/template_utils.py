import os
from app import app


app.jinja_env.globals.update(AMPLITUDE_KEY=os.getenv('AMPLITUDE_KEY'))