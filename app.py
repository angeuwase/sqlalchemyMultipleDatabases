from . import create_app
import sqlite3
from flask import request, make_response, jsonify, g
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy_session import flask_scoped_session
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
import os
#from werkzeug.wrappers import Request
from contextlib import closing
import psycopg2
import functools


app = create_app()
mainDB = SQLAlchemy(app)

## Helper Methods
class User(mainDB.Model):
    __tablename__ = 'users'

    id = mainDB.Column(mainDB.Integer, primary_key=True)
    email = mainDB.Column(mainDB.String(80), unique=True, nullable=False)
    password = mainDB.Column(mainDB.String(120), nullable=False)
    database = mainDB.Column(mainDB.String(120), nullable=False)
    tenantID = mainDB.Column(mainDB.String(120), unique=True, nullable=False)


    def __init__(self, email, password, database, tenantID):
        self.email = email
        self.password = password
        self.database = database
        self.tenantID = tenantID

    def __repr__(self):
        return '<User %r>' % self.email



    
    
    # just do here everything what you need...

## Middleware
@app.before_request
def findTenant():
    # request - flask.request
    tenantID = request.path.split('/')[1]
    print(tenantID)

    tenant = User.query.filter_by(tenantID=tenantID).first()
    if not tenant:
        return 'No tenant'

    database = tenant.database

    print(database)
    
    try: 
        if database == 'postgres':
            conn = psycopg2.connect(
            host="localhost",
            database=tenantID,
            user="postgres",
            password="")

            cur = conn.cursor()

            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)

            g.tenantDB = conn
        
    except (Exception, psycopg2.DatabaseError) as error:
        print('error connecting to DB')
        print(error)
        
@app.teardown_request
def teardown_request(exception):
    g.tenantDB.close()






## Main Application ##

@app.route('/')
def hello():
    mainDB.create_all()
    return 'Starting app'


@app.route('/register', methods=['POST'])
def register():
    
    # get request message payload
    data = request.json

    # check if user already exists
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        try:
            user = User(
                email = data.get('email'),
                password = data.get('password'),
                tenantID = data.get('tenantID'),
                database = data.get('database')
            )
            mainDB.session.add(user)
            mainDB.session.commit()
            responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
            return make_response(jsonify(responseObject)), 201

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

@app.route('/<tenantID>/login', methods=['POST'])
def login(tenantID):

        print('printing tenant id', tenantID)
        
        # get the request message payload
        data = request.get_json()

        try:
            # fetch the user data
            user = User.query.filter_by(
                email = data.get('email')
              ).first()
     
            if user and user.password == data.get('password'):

                responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                    }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500




#@app.before_request
@app.route('/<tenantID>/surveys')
def getTenantSurvey(tenantID):

    conn = g.tenantDB
    cur = conn.cursor()

    cur.execute("SELECT * FROM surveyresults;")
    results = cur.fetchone()
    print("printing database results")
    print(results)

    return 'This is the tenant route'



if '__name__' == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)