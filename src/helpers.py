import datetime
from functools import wraps
import jwt
from flask import request, make_response, current_app as app
from src import db
from src.models import User


def token_required(f):
    """Require valid jwt for a route

    Decorator to protect routes using jwt
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # See if there is an Authorization section in the HTTP request headers
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")

        # If not, then return a 401 error (missing or invalid authentication
            # credentials)
        if not token:
            response = {"message": "Authentication Token missing"}
            return make_response(response, 401)
        # Check the token is valid
        token_payload = decode_auth_token(token)
        user_id = token_payload["sub"]
        # Find the user in the database using their email address which is in
        # the data of the decoded token
        current_user = db.session.execute(
            db.select(User).filter_by(user_id=user_id)).scalar_one_or_none()
        if not current_user:
            response = {"message": "Invalid or missing token."}
            return make_response(response, 401)
        return f(*args, **kwargs)
    return decorator


def encode_auth_token(user_id):
    """Generates the Auth Token

    :param: string user_id  The user id of the user logging in
    :return: string
    """
    try:
        # See https://pyjwt.readthedocs.io/en/latest/api.html for the
        # parameters
        token = jwt.encode(
            # Sets the token to expire in 5 mins
            payload={
                "exp": datetime.datetime.now
                (datetime.UTC) + datetime.timedelta(minutes=5),
                "iat": datetime.datetime.now(datetime.UTC),
                "sub": user_id,
            },
            # Flask app secret key, matches the key used in the decode() in
            # the decorator
            key=app.config['SECRET_KEY'],
            # Matches the algorithm in the decode() in the decorator
            algorithm='HS256'
        )
        return token
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token.
    :param auth_token:
    :return: token payload
    """
    # Use PyJWT.decode(token, key, algorithms) to decode the token with the
    # public key for the app
    try:
        payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"),
                             algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return make_response(
            {'message': "Token expired. Please log in again."}, 401)
    except jwt.InvalidTokenError:
        return make_response(
            {'message': "Invalid token. Please log in again."}, 401)
