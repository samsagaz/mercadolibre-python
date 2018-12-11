import sys
import os
import json

from bottle import Bottle, run, template, route, request
from gevent import monkey
monkey.patch_all()

from mercadolibre.client import Client

APP_ID = '8768460477601196'
APP_SECRET = '1P0eL05XESfzgt2WB5t8VGvAEtMdoi7d'
REDIRECT_URL = 'https://localhost:8000/auth/authorize'

meli = Client(
    client_id=APP_ID,
    client_secret=APP_SECRET,
    site='MLA'
    )

app = Bottle()

@app.route('/')
def index():
    pass

@app.route('/auth/authorize')
def authorize():
    if request.query.get('code'):
        token = meli.exchange_code(
            REDIRECT_URL,
            request.query.get('code')
            )
        print(token)
        meli.set_token(token)
    else:
        return 'ERROR'

@app.route('/auth/login')
def login():
    return "<p>Visit the next <a href='"+meli.authorization_url(REDIRECT_URL)+"'>LINK</a> to get the OAuth Code"

@app.route('/auth/valid_token')
def valid_token():
    return str(meli.is_valid_token)

@app.route('/api/users/me')
def users_me():
    return meli.me()

@app.route('/api/a')
def b():
    return meli.get_available_listing_types_by_category(meli.user_id) 





run(
    app,
    host='localhost',
    port=8000,
    reloader=True,
    server='gevent',
    certfile='server.cert',
    keyfile='server.key'
    )