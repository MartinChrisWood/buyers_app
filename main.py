#!flask/bin/python

# My Example to-do list application

# [START gae_python37_app]

# Flask bits
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Helper function, create a full URI for a property
def make_public_property(house):
	new_house = {}
	
	for field in house:
		new_house[field] = house[field]
		if field == 'id':
			new_house['uri'] = url_for('get_property', property_id=house['id'], _external=True)
	return new_house


# Some fake properties, stored in-memory rather than in an external DB for now
houses = [
			{"id":1,
			 "title": u"Fine 1 bed Flat for Sale!",
			 "address": u"Flat 15, Empress Gardens, Manor Farm Road,  Southampton",
			 "postcode": u"SO31 2FQ",
			 "description": u"Spacious first floor one-bed flat with minor niffler infestation.",
			 "sold": False},
			{"id":2,
			 "title": u"15 Room Mansion going Cheap!",
			 "address": u"Fancy-pants Road, Posh-sods Town, UK",
			 "postcode": u"IS5 2GD",
			 "description": "Gigantic mansion, excellent kitchen, may contain Nigel Farage or relatives.",
			 "sold":False}
		    ]
	
	
@app.route('/properties', methods=['GET'])
def get_properties():
	return( jsonify({'properties': [make_public_property(house) for house in houses]}) )


@app.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
	
	# Filters list of results to properties with matching id number
	house = [house for house in houses if house['id'] == property_id]
	
	# If there's no results, abort and return "not found" HTTP response code
	if len(house) == 0:
		abort(404)
	
	# Weird quirk, line below will only return the first result in the
	# case that there are multiple matches...	
	return( jsonify({'property': house[0]}) )
	
	
@app.route('/properties', methods=['POST'])
def create_property():
	
	if not request.json or not 'title' in request.json:
		abort(400)
	
	house = {'id': houses[-1]['id'] + 1,
			 'title': request.json['title'],
			 'address': request.json.get('address', ""),
			 'postcode': request.json.get('postcode', ""),
			 'description': request.json.get('description', ""),
			 'sold': False}
	
	houses.append(house)
	return( jsonify({'property': house}), 201 )


@app.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
	house = [house for house in houses if house['id'] == property_id]
	
	if len(house) == 0:
		abort(404)
		
	if not request.json:
		abort(400)
	
	if 'title' in request.json and type(request.json['title']) is not unicode:
		abort(400)
		
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
			
	if 'sold' in request.json and type(request.json['sold']) is not bool:
		abort(400)
	
	house[0]['title'] = request.json.get('title', house[0]['title'])
	house[0]['address'] = request.json.get('address', house[0]['address'])
	house[0]['postcode'] = request.json.get('postcode', house[0]['postcode'])
	house[0]['description'] = request.json.get('description', house[0]['description'])
	house[0]['done'] = request.json.get('sold', house[0]['sold'])
	
	return jsonify({'house': house[0]})


@app.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
	house = [house for house in houses if house['id'] == property_id]
	if len(house) == 0:
		abort(404)
	houses.remove(house[0])
	return jsonify({'result': True})
	

# This exists to replace default (human) HTML response in case of 404
# with a more machine-friendly json data dump that could be used by a
# GUI to trigger an appropriate report.
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
	 	

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    
# [END gae_python37_app]
