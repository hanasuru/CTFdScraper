from app import create_app
from flask_jwt_extended import JWTManager
import wtforms_json
import os

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

jwt = JWTManager(app)
wtforms_json.init()

if __name__ == '__main__':
    app.run()