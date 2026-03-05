from flask import Flask
import os

from db import *
import routes

from models.company import Companies


flask_host = os.environ.get('FLASK_HOST')
flask_port = os.environ.get('FLASK_PORT')

database_scheme = os.environ.get('DATABASE_SCHEME')
database_user = os.environ.get('DATABASE_USER')
database_password = os.environ.get('DATABASE_PASSWORD')
database_address = os.environ.get('DATABASE_ADDRESS')
database_port = os.environ.get('DATABASE_PORT')
database_name = os.environ.get('DATABASE_NAME')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'{database_scheme}{database_user}:{database_password}@{database_address}:{database_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

app.register_blueprint(routes.category)
app.register_blueprint(routes.company)
app.register_blueprint(routes.product)
app.register_blueprint(routes.product_category_xref)
app.register_blueprint(routes.warranty)


if __name__ == '__main__':
    app.run(host=flask_host, port=flask_port)