from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.data')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Initialize database
db = SQLAlchemy(app)

#Initialize marshmallow
ma = Marshmallow(app)

# Student Class/ Model
class Student(db.Model):
    mis = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    branch = db.Column(db.String(100))
    contact = db.Column(db.Integer)
    email = db.Column(db.String(100))
    description = db.Column(db.String(200))



    def __init__(self,mis, name, branch, contact, email, description):
        self.mis = mis
        self.name = name
        self.branch = branch
        self.contact = contact
        self.email = email
        self.description = description


#Student Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('mis', 'name', 'branch', 'contact', 'email', 'description')

#Init Schema
student_schema = StudentSchema(strict=True)
students_schema = StudentSchema(many=True, strict=True)

#db.create_all() #--->  Use this line only once, otherwise it will over-write the data again and again

#Create a Product
@app.route('/student', methods=['POST'])
def add_student():
    # mis = request.json['mis']
    # name = request.json['name']
    # branch = request.json['branch']
    # contact = request.json['contact']
    # email = request.json['email']
    # description = request.json['description']

    json_string = request.json
    d = json.loads(json_string)

    mis = d['mis']
    name = d['name']
    branch = d['branch']
    contact = d['contact']
    email = d['email']
    description = d['description']

    new_student = Student(mis, name, branch, contact, email, description)
    #
    db.session.add(new_student)
    db.session.commit()
    #
    # return student_schema.jsonify(new_student)

    return jsonify(request.json)

#Get all products
@app.route('/student', methods=['GET'])
def get_all_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result.data)

#Get a single student data
@app.route('/student/<mis>', methods=['GET'])
def get_student(mis):
    #print(mis)
    student = Student.query.get(mis)
    return student_schema.jsonify(student)

#Update a Product
@app.route('/student/<mis>', methods=['PUT'])
def update_student(mis):
    student = Student.query.get(mis)
    mis = request.json['mis']
    name = request.json['name']
    branch = request.json['branch']
    contact = request.json['contact']
    email = request.json['email']
    description = request.json['description']

    student.mis = mis
    student.name = name
    student.branch = branch
    student.contact = contact
    student.email = email
    student.description = description


    db.session.commit()

    return student_schema.jsonify(student)

#Delete a product
@app.route('/student/<mis>', methods=['DELETE'])
def delete_product(mis):
    student = Student.query.get(mis)
    db.session.delete(student)

    db.session.commit()

    return student_schema.jsonify(student)

#Run server
if __name__ == '__main__':
    app.run(debug=True)
