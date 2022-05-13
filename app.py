from flask import Flask
from restaurant.handler import restaurant
from menu.handler import menu
from order.handler import order

import database

app = Flask(__name__)


app.register_blueprint(restaurant)
app.register_blueprint(menu)
app.register_blueprint(order)

if __name__ == "__main__":
    app.run(debug=True)
