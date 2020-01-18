from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    # look in the database instead of the mapping as before
    user = UserModel.find_by_username(username)
    
    # safer way of comparing strings
    if user and safe_str_cmp(user.password, password):
        return user

# payload is the content of the JWT token
def identity(payload):
    # extract user_id from the payload
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)