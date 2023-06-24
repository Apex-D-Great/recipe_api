from flask import Flask, jsonify
from flask_restx import Api, Resource
from backend.models import db, Recipe
from .config import DevConfig,TestConfig,ProdConfig
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .routes.Recipe import recipe_ns

import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()


app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SERVER_NAME'] = 'localhost:5000'

JWTManager(app)
CORS(app)

# db_init
db.init_app(app)
app.app_context().push()
db.create_all()

migrate = Migrate(app,db)
# with app.app_context():
#     if db.engine.url.drivername == "sqlite":
#         migrate.init_app(app, db, render_as_batch=True)
#     else:
#         migrate.init_app(app, db)

oauth = OAuth(app)

from .Auth import auth_ns

api.add_namespace(recipe_ns)
api.add_namespace(auth_ns)




@app.shell_context_processor
def make_shell_context():
    return {"db":db, "recipe":Recipe}

# @api.route("/hello")
# class HelloResource(Resource):
#     def get(self):
#         return jsonify({"hello":"hy"})

