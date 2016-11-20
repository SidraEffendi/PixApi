from flask import Flask, render_template, request, redirect, jsonify, json, abort,g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pixdb_setup import Photos, Events, User, Base

from flask_httpauth import HTTPBasicAuth
import json

#NEW IMPORTS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

auth = HTTPBasicAuth()


app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://postgres:XxxAahSn@2*5@localhost/pixtest')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']

@auth.verify_password
def verify_password(emailid_or_token, username):
    #Try to see if it's a token first
    user_email_id = User.verify_auth_token(emailid_or_token)
    if user_email_id:
        user = session.query(User).filter_by(email_id = user_email_id).one()
    else:
        user = session.query(User).filter_by(email_id = emailid_or_token).first()
        if not user:
            return False
    g.user = user
    return True


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})



@app.route('/users/<username>/<email_id>', methods = ['POST'])
def new_user(username,email_id):
    #username = request.json.get('username')
    #email_id = request.json.get('email_id')
    if username is None or email_id is None:
        print ("missing arguments")
        abort(400) 
        
    if session.query(User).filter_by(email_id = email_id).first() is not None:
        print ("existing user")
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
        
    user = User(email_id = email_id,username = username)
    #user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'email_id': user.email_id }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<email_id>')
def get_user(email_id):
    user = session.query(User).filter_by(email_id=email_id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

## To get the events associated witha particular user ##
@app.route('/pixget/<email_id>/elist')
def dataJSON_get(email_id):
	hosted_events = session.query(Events.code_id).filter_by(event_email_id =email_id).all()
	as_guest = session.query(User.guest_code_id).filter_by(email_id =email_id).all()
	#return jsonify({'event_email_id': hosted_events}) This works
	return jsonify({'guest_code_id': as_guest, 'hosted_events': hosted_events})

## To check if an event id guest entered exists##
@app.route('/pixget/<event_id>/event')
def dataJSON_getEventCheck(event_id):
	event_e = session.query(Events).filter_by(code_id=event_id)
	if event_e is not None:
		checked = 1
		return str(checked)
	else:	
		return 

@app.route('/pixpost/events/<email_id>', methods = ['GET', 'POST'])
def dataJSON_post(email_id):
	if request.method == 'GET':
    # RETURN ALL DATA IN DATABASE
		user_d = session.query(User).filter_by(email_id =email_id)
		items = session.query(Events).filter_by(event_email_id =email_id)
		return jsonify(Events=[i.serialize for i in items])

	elif request.method == 'POST':
    # MAKE A NEW DATA COLUMN AND STORE IT IN DATABASE
        #if request.headers['Content-Type'] == 'application/json':
		user_i = session.query(User).filter_by(email_id =email_id).one()
		tempo =request.json["code_id"]
		starr = []
		starr.append(tempo)
		if user_i.admin_code_id is not None:
			user_i.admin_code_id = starr + user_i.admin_code_id 
		else:
			user_i.admin_code_id = starr
		#return ''.join(user_i.admin_code_id)
		session.commit()
		data_item = Events(code_id = request.json["code_id"], event_type = request.json["event_type"], album_name = request.json["album_name"],
        	event_date= request.json["event_date"], event_loc= request.json["event_loc"],bucket_link= request.json["bucket_link"],
        	event_email_id=user_i.email_id)
		session.add(data_item)
		session.commit()
		items = session.query(Events).all()
		return jsonify(Events=[i.serialize for i in items])

@app.route('/pixget/photos/<event_id>/count')
def dataJSON_getPhotoCount(event_id):
	#event = session.query(Events).filter_by(code_id=event_id).one()
	photos_e = session.query(Photos).filter_by(photo_code_id=event_id)
	tempo = photos_e.count()
	if tempo == 0:
		return
	else:	
		return str(photos_e.count())
    #items = session.query(Photos).all()
    #return jsonify(Photos=[i.serialize for i in items])

@app.route('/pixpost/photos/<event_id>', methods = ['GET', 'POST'])
def dataJSON_postPhotos(event_id):
	if request.method == 'GET':
    # RETURN ALL DATA IN DATABASE
		event = session.query(Events).filter_by(code_id=event_id).one()
		photos_e = session.query(Photos).filter_by(photo_code_id=event.code_id)
		return jsonify(Photos=[i.serialize for i in photos_e])
		#return str(photos_e.count())

	elif request.method == 'POST':
    # MAKE A NEW DATA COLUMN AND STORE IT IN DATABASE
        #if request.headers['Content-Type'] == 'application/json':
		photo1 = Photos(photo_code_id = event_id, image_url = request.json["image_url"])
		session.add(photo1)
		session.commit()
		event = session.query(Events).filter_by(code_id=event_id).one()
		photos_e = session.query(Photos).filter_by(photo_code_id=event.code_id)
		return jsonify(Photos=[i.serialize for i in photos_e])
		#items = session.query(Photos).all()
    	#return jsonify(Photos=[i.serialize for i in items])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)