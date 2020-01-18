from db import db

# note that ItemModel extends db.Model
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel") # basically a join on id. Automatically matches store_id with store.id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # equivalent to: SELECT * FROM items WHERE name=name LIMIT 1
        # this returns and ItemModel object
        return cls.query.filter_by(name=name).first() # .query is a query builder

    # this method is now able both insert and updating -- "upserting". We got rid of the update method
    def save_to_db(self):
        # session is a collection of objects that we're writing to the database. 
        # We can add multiple objects and save at the same time, but here we just add self
        db.session.add(self)
        # save to the database
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()