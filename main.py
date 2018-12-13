#!flask/bin/python

# RESTful properties web service

# [START gae_python37_app]

# Flask bits
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import pymongo

# Set up the app
app = Flask(__name__)

# Set up CORS (allow from anywhere)
CORS(app)

# Set up the database connection
MONGO_HOST = "35.187.119.75"
MONGO_DB = "properties"

# Connect to the database
cl = pymongo.MongoClient(MONGO_HOST + ":27017")
db = cl['ryanprop']
col = db['properties']


@app.route('/properties', methods=['GET'])
def get_properties():
	
	# Get the properties data, drop object ID's (they don't jsonify...)
	houses = [{key:value for key, value in house.items() if key != "_id"} for house in col.find()]
	
	# Return the properties after appending URI data
	return( jsonify({'properties': houses}) )


@app.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
	
	# Filters list of results to the property with matching id number
	house = col.find_one({"id":property_id})
	
	house.pop("_id")
	
	# If there's no results, abort and return "not found" HTTP response code
	if len(house) == 0:
		abort(404)
	
	return( jsonify({'property': house}) )
	
	
@app.route('/properties', methods=['POST'])
def create_property():
	
	if not request.json or not 'title' in request.json:
		abort(400)
	
	house = {'id': col.find.count() + 1,
			 'title': request.json['title'],
			 'address': request.json.get('address', ""),
			 'postcode': request.json.get('postcode', ""),
			 'description': request.json.get('description', ""),
			 'sold': False}
	
	col.insert(house)
	return( jsonify({'property': house}), 201 )


@app.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):

	# Filters list of results to the property with matching id number
	house = col.find_one({"id":property_id})
	
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
	
	house['title'] = request.json.get('title', house[0]['title'])
	house['address'] = request.json.get('address', house[0]['address'])
	house['postcode'] = request.json.get('postcode', house[0]['postcode'])
	house['description'] = request.json.get('description', house[0]['description'])
	house['done'] = request.json.get('sold', house[0]['sold'])
	
	# Update the database
	col.update({"id":property_id}, house)
	
	return jsonify({'house': house})


@app.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):

	# Filters list of results to the property with matching id number
	house = col.find_one({"id":property_id})
	
	if len(house) == 0:
		abort(404)
	
	# Delete record from the database
	col.delete({"_id":house["_id"]})
	
	return jsonify({'result': True})
	

# This exists to replace default (human) HTML response in case of 404
# with a more machine-friendly json data dump that could be used by a
# GUI to trigger an appropriate report.
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    
# [END gae_python37_app]
