from flask import Flask, render_template, request, redirect, jsonify, json, abort,g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pixdb_setup import Photos, Events, Base


app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://postgres:XxxAahSn@2*5@localhost/pixtest')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

## To get the data in the events table ##
@app.route('/pixget')
def dataJSON_get():
    items = session.query(Events).all()
    return jsonify(Events=[i.serialize for i in items])

@app.route('/pixget/<event_id>')
def dataJSON_getEventCheck(event_id):
	event_e = session.query(Events).filter_by(code_id=event_id)
	if event_e is not None:
		checked = 1
		return str(checked)
	else:	
		return 

@app.route('/pixpost/events', methods = ['GET', 'POST'])
def dataJSON_post():
	if request.method == 'GET':
    # RETURN ALL DATA IN DATABASE
		items = session.query(Events).all()
		return jsonify(Events=[i.serialize for i in items])

	elif request.method == 'POST':
    # MAKE A NEW DATA COLUMN AND STORE IT IN DATABASE
        #if request.headers['Content-Type'] == 'application/json':
		data_item = Events(code_id = request.json["code_id"], event_type = request.json["event_type"], album_name = request.json["album_name"],
        	event_date= request.json["event_date"], event_loc= request.json["event_loc"],bucket_link= request.json["bucket_link"])
		session.add(data_item)
		session.commit()
		items = session.query(Events).all()
		return jsonify(Events=[i.serialize for i in items])

@app.route('/pixget/photos/<event_id>')
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