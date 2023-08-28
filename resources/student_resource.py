from flask_restful import Resource, reqparse
from database import SessionLocal, Student
from flask_jwt_extended import jwt_required


class StudentResource(Resource):

    @jwt_required()
    def get(self, student_id=None):
        db = SessionLocal()
        student = db.query(Student).filter(Student.id == student_id).first()
        print(student_id, "ppppp")
        print(student, "ooooooooo")
        db.close()
        if student:
            return {"id": student.id, "name": student.name, "age": student.age}
        return {"message": "Student not found"}, 404

    @jwt_required()
    def get(self):
        db = SessionLocal()
        students = db.query(Student).all()
        db.close()
        student_data = []
        if students:
            for student in students:
                student_dict = {
                    'id': student.id,
                    'name': student.name,
                    'age': student.age
                    }

                student_data.append(student_dict)
            return student_data
        return {"message": "Student not found"}, 404

    def post(self):
        db = SessionLocal()
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("age", type=int, required=True)
        parser.add_argument("password", type=str, required=True)
        data = parser.parse_args()
        student = Student(name=data['name'], age=data['age'], password=data['password'])
        db.add(student)
        db.commit()
        db.close()
        return {"message": "Student Posted"}

    def put(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("age", type=int, required=True)
        data = parser.parse_args()

        db = SessionLocal()
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            student.name = data["name"]
            student.age = data["age"]
            db.commit()
            db.close()
            return {"message": "Student updated"}
        db.close()
        return {"message": "Student not found"}, 404

    def delete(self, student_id):
        db = SessionLocal()
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            db.delete(student)
            db.commit()
            db.close()
            return {"message": "Student deleted"}
        db.close()
        return {"message": "Student not found"}, 404
