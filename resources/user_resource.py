from flask_restful import Resource, reqparse
from flask import jsonify
from database import SessionLocal
from database.models import User
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, create_refresh_token


def hash_password(password):
    return sha256.hash(password)


def verify_password(password, hashed_password):
    return sha256.verify(password, hashed_password)


plain_password = "mysecretpassword"
hashed_password = hash_password(plain_password)

if verify_password(plain_password, hashed_password):
    print("Password is correct")
else:
    print("Password is incorrect")


class UserSignUpResource(Resource):
    def post(self):
        db = SessionLocal()
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        data = parser.parse_args()
        hashed_password = hash_password(data['password'])
        user = User(username=data['username'], password=hashed_password)
        db.add(user)
        db.commit()
        db.close()
        return {"message": "User Sign-up"}


class UserSignInResource(Resource):
    def post(self):
        db = SessionLocal()
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        data = parser.parse_args()

        user = db.query(User).filter(User.username == data['username']).first()
        db.close()

        if user and verify_password(data['password'], user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
