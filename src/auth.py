from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from src.database import User,bookmark,db
import validators
from flask_jwt_extended import get_jwt_identity,create_access_token,create_refresh_token
from flasgger.utils import swag_from

auth=Blueprint('auth',__name__,url_prefix='/api/v1/auth')


@auth.post('/register')
@swag_from('docs/auth/register.yml')
def register1():
    name=request.json.get('name')
    email=request.json.get('email')
    password=request.json.get('password')
    if not name:
        return jsonify({'message':'please give all required info'}),206
    if not email:
        return jsonify({'message':'please give all required info'}),206
    if not password:
        return jsonify({'message':'please give all required info'}),206
    pwd=generate_password_hash(password)
    users=User.query.filter_by(email=email).first()
    user_name=User.query.filter_by(name=name).first()
    if not validators.email(email):
        return jsonify({'message':'Please enter a valid email'}),406
    if not validators.between(len(password),min=8):
        return jsonify({'message':'password should be greater than 8'}),411
    if user_name:
        return jsonify({'message':'This user name is already exists'}),409
    if users:
        return jsonify({'message':'This email is already exists'}),409
    

    user=User(name=name,email=email,password=pwd[14:])
    db.session.add(user)
    db.session.commit()
    user_id=User.query.filter_by(email=email).first()
    access=create_access_token(identity=user_id.id)
    return jsonify({'meaasege':'User Created','user':{'username':name,'email':email},'access token':access}),201

@auth.post('/login')
@swag_from('docs/auth/login.yml')
def login():
    email=request.json.get('email')
    password=request.json.get('password')
    if not email:
        return jsonify({'message':'please give all required info'}),206
    if not password:
        return jsonify({'message':'please give all required info'}),206
    user=User.query.filter_by(email=email).first()
    if user:
        if check_password_hash('pbkdf2:sha256:'+user.password, password):
            access=create_access_token(identity=user.id)
            return jsonify({'message':f'{user.name} is logined','user':{'name':user.name,'email':user.email},'access token':access}),200
        else:
            return jsonify({'message':'Please enter Correct Password'}),203
    else:
        return jsonify({'message':'User Not Existed. Create a User'}),404
