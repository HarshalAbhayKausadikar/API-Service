import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.data')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Database for storing history of operations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.history_data')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Initialize database
db = SQLAlchemy(app)

#Initialize database for storing history of operations
history_db = SQLAlchemy(app)

#Initialize marshmallow
ma = Marshmallow(app)

#Initialize marshmallow for history
ma2 = Marshmallow(app)

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

#History Class/ Model
class History(history_db.Model):
    user_mis = history_db.Column(history_db.Integer, primary_key=True)
    username_who_requested = history_db.Column(history_db.String(100))
    type_of_request = history_db.Column(history_db.String(100))
    data_associated = history_db.Column(history_db.String(1000))


    def __init__(self, user_mis, username_who_requested, type_of_request, data_associated):
        self.user_mis = user_mis
        self.username_who_requested = username_who_requested
        self.type_of_request = type_of_request
        self.data_associated = data_associated

#Student Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('mis', 'name', 'branch', 'contact', 'email', 'description')

#History Schema
class HistorySchema(ma2.Schema):
    class Meta2:
        history_fields = ('user_mis', 'username_who_requested', 'type_of_request', 'data_associated')

#Init Schema
student_schema = StudentSchema(strict=True)
students_schema = StudentSchema(many=True, strict=True)

#Init History Schema
history_schema = HistorySchema(strict=True)
history_schema_all = HistorySchema(many=True, strict=True)

#db.create_all() #--->  Use this line only once, otherwise it will over-write the data again and again
#history_db.create_all()

#Create a Product
@app.route('/student', methods=['POST'])
def add_student():
    mis = request.json['mis']
    name = request.json['name']
    branch = request.json['branch']
    contact = request.json['contact']
    email = request.json['email']
    description = request.json['description']

    d = {'type_of_request':'POST'}

    user_mis = mis
    username_who_requested = name
    type_of_request = d['type_of_request']
    #data_associated = "test_string"
    #data_associated = ""
    data_associated = json.dumps(request.json)

    print(user_mis)
    print(data_associated)

    history_new = History(user_mis, username_who_requested, type_of_request, data_associated)
    print(history_new)
    history_db.session.add(history_new)
    history_db.session.commit()

    new_student = Student(mis, name, branch, contact, email, description)

    db.session.add(new_student)
    db.session.commit()


    return student_schema.jsonify(new_student)

#Get all students
@app.route('/student', methods=['GET'])
def get_all_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)

    return jsonify(result.data)

#Get a single product
@app.route('/student/<mis>', methods=['GET'])
def get_student(mis):
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

#Get all history
@app.route('/history', methods=['GET'])
def get_history():
    all_history = History.query.all()
    print(all_history)
    print(all_history[2].user_mis)
    print(all_history[2].username_who_requested)
    print(all_history[2].type_of_request)
    print(all_history[2].data_associated)
    result_history = history_schema_all.dump(all_history)
    print(result_history)
    return jsonify(result_history.data)

#Run server
if __name__ == '__main__':
    app.run(debug=True)
