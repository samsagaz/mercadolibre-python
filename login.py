from gevent import monkey
# Patch to allow SSL Working
monkey.patch_all()

import sys
import os
import json
import requests
import webbrowser
from bottle import (
    Bottle,
    run,
    template,
    route,
    request,
    view,
    jinja2_view,
    TEMPLATE_PATH)

from mercadolibre.client import Client


TEMPLATE_PATH[:] = ['templates']
APP_ID = '8768460477601196'
APP_SECRET = '1P0eL05XESfzgt2WB5t8VGvAEtMdoi7d'
LOCAL_URI = 'https://localhost:8000'
REDIRECT_URI = 'https://localhost:8000/auth/authorize'

meli = Client(
    client_id=APP_ID,
    client_secret=APP_SECRET,
    site='MLA'
    )

app = Bottle()

@app.route('/auth/authorize')
def authorize():
    if request.query.get('code'):
        token = meli.exchange_code(
            REDIRECT_URI,
            request.query.get('code')
            )
        meli.set_token(token)
        webbrowser.open('https://localhost:8000/', new=0, autoraise=True) 
    else:
        return 'ERROR'

@app.route('/auth/valid_token')
def valid_token():
    return str(meli.is_valid_token)
    
@app.route('/')
@jinja2_view('home.html')
def index():
    users = [] 
    auth_url = ''
    auth_url =  "<p>Visit the follow URL to <a href='"+meli.authorization_url(REDIRECT_URI)+"'>Get Auth Token</a> to access MercadoLibre"    
    if meli.access_token:
        users.append('<a href="'+LOCAL_URI+'/users/me" target="_blank">users/me</a>')
        users.append('<a href="'+LOCAL_URI+'/users/'+str(meli.user_id)+'" target="_blank">users/{Cust_id}</a>')
        users.append('<a href="'+LOCAL_URI+'/users/'+str(meli.user_id)+'/addresses" target="_blank">users/{Cust_id}/addreses</a>')
        users.append('<a href="'+LOCAL_URI+'/users/'+str(meli.user_id)+'/accepted_payment_methods" target="_blank">users/{Cust_id}/accepted_payment_methods</a>')
        
        users.append('<a href="'+LOCAL_URI+'/users/{Cust_id}" target="_blank">users/{Cust_id}</a>')
        users.append('<a href="'+LOCAL_URI+'/users/{Cust_id}" target="_blank">users/{Cust_id}</a>')
        users.append('<a href="'+LOCAL_URI+'/users/{Cust_id}" target="_blank">users/{Cust_id}</a>')
        users.append('<a href="'+LOCAL_URI+'/users/{Cust_id}" target="_blank">users/{Cust_id}</a>')
        users.append('<a href="'+LOCAL_URI+'/users/{Cust_id}" target="_blank">users/{Cust_id}</a>')
    return {
        'auth_url': auth_url,
        'users': users,
    }

@app.route('/users/me')
def users_me():
    # /users/me
    return meli.me()

@app.route('/users/<id>')
def get_user(id):
    return meli.get_user(id)

@app.route('/users/<id>/addresses')
def get_user(id):
    return meli.get_user_address(id)

@app.route('/users/<id>/accepted_payment_methods')
def get_user(id):
    return meli.get_user_accepted_payment_methods(id)


@app.route('/api/a')
def b():
    # return meli.get_category_predictor(meli.user_id) 
    return meli.get_classifield_promotion_packs_by_category('MLA1743')

run(
    app,
    host='127.0.0.1',
    port=8000,
    reloader=True,
    server='gevent',
    certfile='server.cert',
    keyfile='server.key'
    )