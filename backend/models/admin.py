# from pymongo import MongoClient
# import bcrypt
# import jwt
# import datetime
#
# # Initialize Bcrypt
# bcrypt = Bcrypt()
#
# def authenticate_user(username, password, secret_key):
#     user = users_collection.find_one({"username": username})
#
#     if not user or not bcrypt.check_password_hash(user['password'], password):
#         return None
#
#     # Generate the token
#     token = jwt.encode({
#         'public_id': str(user['_id']),
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
#     }, secret_key)
#
#     return token
#
# def get_user(username):
#     user = users_collection.find_one({"username": username}, {"password": 0})  # Exclude password from the result
#     return user