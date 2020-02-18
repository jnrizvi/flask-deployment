import os

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db
import random


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False # turn off Flask_SQLAlchemy modfication tracker because SQL_Alchemy already has one
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "sqlite:///data.db") # we can still use sqlite locally if the environment variable for Postgres is not found
db.init_app(app)

app.secret_key = 'jawad'
api = Api(app) # allow us to easily add resources

# We got rid of the create_tables.py script for this
@app.before_first_request # decorator directly from Flask!
def create_tables():
    db.create_all() # only creates the tables that it SEES


# JWT object creates a new endpoint /auth
# When we call /auth, we send it a username and a password
# The JWT sends that username and password to the authenticate function, which takes those as arguments
jwt = JWT(app, authenticate, identity)

# these resources are now accessible by our api, by their respective endpoints
# items table
# We add the Item resource, which imports the Item model, which has __tablename__ = "items"
# along with the column definitions. If you don't have a resource associated with something you want to store in a db, you can also just import a model directly
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
# users table
api.add_resource(UserRegister, '/register')
# stores table
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')



# in-memory database
notfications = []

# every resource you create has to be a class
class Notification(Resource):
    parser = reqparse.RequestParser()
    # make sure the description argument is there
    parser.add_argument('description',
        type=str
    )

    def post(self):
        # clear errors first before loading data
        # if next(filter(lambda x: x['id'] == id, notfications), None) is not None:
        #     return {'message': "An notification with id '{}' already exists.".format(id)}, 400 # bad request
        
        # save the request data payload into the variable 'data' 
        request_data = request.get_json()
        print(request_data)
        data = Notification.parser.parse_args()
        
        id = random.getrandbits(128)
        
        # notification = {'id': id, 'description': data['description']}
        notification = {
          'manage_url': request_data['manage_url'],
          'memo': request_data['memo'],
          'src_ip': request_data['additional_data']['src_ip'],
          'useragent': request_data['additional_data']['useragent'],
          'referer': request_data['additional_data']['referer'],
          'location': request_data['additional_data']['location'],
          'channel': request_data['channel'],
          'time': request_data['time']
        }
        
        notfications.append(notification)
        return notification, 201

class NotificationList(Resource):
    def get(self):
        return {'notifications': notfications}


api.add_resource(Notification, '/newnotification')
api.add_resource(NotificationList, '/notifications')

# avoid running the app on importing app. Only the file you run is __main__
if __name__ == '__main__':
    app.run(port=5000, debug=True)