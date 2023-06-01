#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
if getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_request() -> str:
    """a method to handler before_request"""
    if auth is None:
        return
    if not auth.require_auth(path=request.path, excluded_paths=[
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/']):
        return
    if (not auth.authorization_header(request) and
            not auth.session_cookie(request)):
        abort(401)
    if not auth.current_user(request):
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """a method that handles unauthorized errors"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """a method that handles forbidden errors"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)