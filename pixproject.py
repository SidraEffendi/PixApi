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

@app.route('/pixpost/new', methods = ['GET', 'POST'])
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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)