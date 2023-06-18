from flask_restx import Namespace, Resource, fields
from flask import jsonify, make_response, render_template, url_for
from .models import User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from backend import oauth


load_dotenv()


auth_ns = Namespace("auth", description="everything authentication endpoint which also include google authentication")

signup_model = auth_ns.model(
    "Signup",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(),
        "password": fields.String(),
    }
)


@auth_ns.route("/signup")
class Signup(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        """sign up method"""
        data = request.get_json()
        user = User.query.filter_by(username=data.get("email")).first()
        if user:
            return jsonify({"message":"email already exist in our database, use a new valid email"})
        password = generate_password_hash(data.get("password"))
        new_user = User(username=data.get("username"), email=data.get("email"), password=password)
        new_user.save()
        return make_response(jsonify({"message":"user created successfully"}),201)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """login method"""
        data = request.get_json()
        print(data.get("password"))
        user = User.query.filter_by(email=data.get("email")).first()
        if user is not None and check_password_hash(user.password,data.get("password")):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({"access_token":access_token, "refresh_token":refresh_token, "message":f"welcome {user.username}"})
        return jsonify({"message":"incorrect credentials or you probably dont have an account, sign up"})
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("login.html"),200,headers)


# The user details get print in the console.
# so you can do whatever you want to do instead
# of printing it


'''
	Set SERVER_NAME to localhost as twitter callback
	url does not accept 127.0.0.1
	Tip : set callback origin(site) for facebook and twitter
	as http://domain.com (or use your domain name) as this provider
	don't accept 127.0.0.1 / localhost
'''



# @auth_ns.route('/')
# def index():
# 	return render_template('index.html')

@auth_ns.route('/login/google/')
class google_login(Resource):
    def get(self):
        # Google Oauth Config
        # Get client_id and client_secret from environment variables
        # For developement purpose you can directly put it
        # here inside double quotes
        try:
            GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
            GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
            
            CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
            oauth.register(
                name='google',
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                server_metadata_url=CONF_URL,
                client_kwargs={
                    'scope': 'openid email profile'
                }
            )
            # Redirect to google_auth function
            redirect_uri = url_for('auth_google_auth', _external=True)
            return oauth.google.authorize_redirect(redirect_uri)
        except:
            return make_response(jsonify({"message":"Connection refused by the server.."}), 500)

@auth_ns.route('/login/google/auth/')
class google_auth(Resource):
    def get(self):
        token = oauth.google.authorize_access_token()
        user = token['userinfo']
        new_user = User(username=user["name"], email=user["email"], password=user["email"])
        new_user.save()
        user = User.query.filter_by(email=user["email"]).first()
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        print(access_token)
        # return jsonify({"access_token":access_token, "refresh_token":refresh_token})
        return "you are in"
        

