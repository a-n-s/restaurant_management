from pymongo import MongoClient
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.5wgh4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.restaurant_management
