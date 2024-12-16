from pymongo import MongoClient

# Создание клиента MongoDB
client: MongoClient = MongoClient("mongodb://mongo:27017")

# Инициализация базы данных и коллекций
db = client.car_database
car_collection = db.cars
registration_collection = db.registrations
users_collection = db.users
