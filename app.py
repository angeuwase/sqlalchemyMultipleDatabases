from . import create_app
from flask import request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy



app = create_app()
mainDB = SQLAlchemy(app)


## Database ##

class User(mainDB.Model):
    __tablename__ = 'users'

    id = mainDB.Column(mainDB.Integer, primary_key=True)
    email = mainDB.Column(mainDB.String(80), unique=True, nullable=False)
    password = mainDB.Column(mainDB.String(120), unique=True, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email


## Main Application ##

@app.route('/')
def hello():
    mainDB.create_all()

    return 'Hello, World!!'

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
                password = data.get('password')
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

@app.route('/login', methods=['POST'])
def login():
        
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


if '__name__' == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)