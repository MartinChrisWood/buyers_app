import pymongo

MONGO_HOST = "35.187.119.75"
MONGO_DB = "properties"

# Connect to the database
cl = pymongo.MongoClient(MONGO_HOST + ":27017")
db = cl['ryanprop']
col = db['properties']

# Wipe the database
col.delete_many({})

# Create a bunch of fake records
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
			 "sold":False},
			{"id":3,
			 "title": u"Cozy modern single-space dwelling in London!",
			 "address": u"(under) The Bridge, London, UK",
			 "postcode": u"IS5 2GD",
			 "description": "Modern layout single living space, corrugated walls, some damp problems, is a cardboard box.  But London!",
			 "sold":False}
		    ]

# Upload said fake data
for each in houses:
	col.insert(each)
