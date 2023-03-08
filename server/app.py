from flask import Flask
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

from routes import leaderboard_single
from routes import leaderboard_averages

if __name__ == '__main__':
  app.run()