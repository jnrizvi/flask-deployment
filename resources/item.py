from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# every resource you create has to be a class. Changes here modify the api
class Item(Resource):
    # parser belongs to Item class itself, as opposed to one specific method
    parser = reqparse.RequestParser()
    # make sure the price argument is there
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    # make sure the store_id argument is there
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )    

    # for verification, you can put this @jwt_required() decorator before any of these methods, and they will require a jwt token and authorization header to be executed
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404


    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # bad request
        
        # save the json payload into the variable data 
        # data = request.get_json() 
        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'], data["store_id"])
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500  # internal server error, not user's fault

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # print(data['another'])
        
        item = ItemModel.find_by_name(name) # NOT a row of a database. Just a python object
        
        
        if item is None: 
            # not found in db, make a new one
            item = ItemModel(name, data['price'], data["store_id"])
        else:
            item.price = data['price']
        
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # better to use do:
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {"items": [item.json() for item in ItemModel.query.all()]}