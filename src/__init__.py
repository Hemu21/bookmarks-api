from flask import Flask,config,jsonify
from dotenv import load_dotenv
from src.auth import auth
from src.database import db
from src.constants.http_status_codes import *
from flask_sqlalchemy import SQLAlchemy
import os
from src.book import book
from flask_jwt_extended import JWTManager
from datetime import timedelta
from  flasgger import Swagger
from flask_cors import CORS
from src.config.swagger import template,swagger_config

def create_app(test_config=None):
    
    app=Flask(__name__,instance_relative_config=True)
    if test_config == None:
        load_dotenv()
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DB_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
            JWT_SECRET_KEY=os.environ.get('jwt_secret_key'),
            SWAGGER={
                'title':"Bookmarks API",
                'uiversion':3
            }

            )
    else:
        app.config.from_mapping(test_config)
    
    db.app=app
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(book)
    jwt=JWTManager(app)
    cors=CORS(app)
    Swagger(app,config=swagger_config,template=template)    
    @app.errorhandler(404)
    def handle(e):
        return jsonify({'error':'Not Found'}),404
    @app.errorhandler(405)
    def handle1(e):
        return jsonify({'error':'Method Not Allowed'}),405
    @app.errorhandler(500)
    def handle2(e):
        return jsonify({'error':'Something went wrong, we are working on it'}),500
    @app.errorhandler(TypeError)
    def handle_type_error(error):
        response = jsonify({
            'error': 'Type error: {}'.format(str(error))
        })
        response.status_code = 400
        return response
    return app
