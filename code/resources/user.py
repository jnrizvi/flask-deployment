import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    # parser belongs to UserRegister class itself, as opposed to one specific method
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        # Now we have to use the parser. The parser expects a username and a password as arguments
        data = UserRegister.parser.parse_args() # part of FlaskRESTful

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data["username"], data["password"])
        user.save_to_db()

        return {"message": "User created successfully."}, 201