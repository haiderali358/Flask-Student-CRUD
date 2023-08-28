from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.student_resource import StudentResource
from resources.user_resource import UserSignUpResource, UserSignInResource
from database.databases import engine, Base

app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'abc123'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=600)

jwt = JWTManager(app)

Base.metadata.create_all(bind=engine)

api.add_resource(StudentResource, "/student/<int:student_id>", "/students")
api.add_resource(UserSignUpResource, "/user/sign_up")
api.add_resource(UserSignInResource, "/user/sign_in")

if __name__ == "__main__":
    app.run(debug=True)
