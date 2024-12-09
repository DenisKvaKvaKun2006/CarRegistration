from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")
db = client.car_database
car_collection = db.cars
registration_collection = db.registrations
users_collection = db.users
