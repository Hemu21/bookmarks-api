from flask import Blueprint,request,jsonify,redirect,url_for
from src.database import User,bookmark,db
from random import choices
from flask_jwt_extended import jwt_required,get_jwt_identity
import string
import webbrowser
from flasgger.utils import swag_from
import validators
import os
from dotenv import load_dotenv

l=[]
load_dotenv()
book = Blueprint('book', __name__,url_prefix='/api/v1/bookmarks')
def url_short():
    global l
    url=string.digits+string.ascii_lowercase
    short_url=''.join(choices(url,k=3))
    if short_url not in l:
        l.append(short_url)
        return short_url
    else:
        return url_short()

@book.get('/list')
@jwt_required()
@swag_from('docs/bookmark/get_all.yml')
def book_list():
    user_id=get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    booklist=bookmark.query.filter_by(user_id=user_id).all()
    if not booklist:
        return jsonify({'message':'No bookmarks available'}),404
    l={'user name':user.name}
    for i in range(len(booklist)):
        l[str(i+1)]={}
        l[str(i+1)]['short_url']=booklist[i].short_url

    return jsonify(l)

@book.get('/list/<string:short_url>')
@jwt_required()
@swag_from('docs/bookmark/get_short_url.yml')
def show(short_url):
    book=bookmark.query.filter_by(short_url=short_url).first()
    if not book:
        return jsonify({'message':'short_url is not in your bookmarks'}),404
    webbrowser.open(book.url)
    book.views+=1
    db.session.commit()
    return redirect(book.url),200 

@book.put('/list/url/<string:short_url>')
@jwt_required()
@swag_from('docs/bookmark/put_url.yml')
def update_url(short_url):
    book=bookmark.query.filter_by(short_url=short_url).first()
    if not book:
        return jsonify({'message':'short url not found in your bookmarks'}),404
    if not request.json['url']:
        return jsonify({'message':'please give all required info'}),206
    if book.url==request.json['url']:
        return jsonify({'message':'old and new urls are same'}),409
    

    book.url=request.json['url']
    db.session.commit()
    return jsonify({'message':'url is updated'}),202

@book.put('/list/short_url/<string:short_url>')
@jwt_required()
@swag_from('docs/bookmark/put_short_url.yml')
def update_short_url(short_url):
    book=bookmark.query.filter_by(short_url=short_url).first()
    if not book:
        return jsonify({'message':'short url not found in your bookmarks'}),404
    book.short_url=url_short()
    db.session.commit()
    return jsonify({'message':'short url is updated'}),202



@book.post('/add')
@jwt_required()
@swag_from('docs/url.yml')
def book_add():
    user_id=get_jwt_identity()
    url=request.json.get('url')
    short_url = url_short()
    if not url:
        return jsonify({'message':'please give all required info'}),206
    if not validators.url(url):
        return jsonify({'message':'Invalid Url'}),400
    user=User.query.filter_by(id=user_id).first()
    existbook=bookmark.query.filter_by(url=url,user_id=user_id).first()
    if existbook:
        return jsonify({'message':'This url is already existed!'}),409
    bookmk=bookmark(url=url,short_url=short_url,user_id=user.id)
    db.session.add(bookmk)
    db.session.commit()
    return jsonify({'message':'bookmark is created',
    'bookmark':{'user name':user.name,'short_url':short_url}}
    ),202

@book.delete('/delete')
@jwt_required()
@swag_from('docs/bookmark/delete_all.yml')
def book_delete():
    user_id=get_jwt_identity()
    bookmk=bookmark.query.filter_by(user_id=user_id).all()
    if not bookmk:
        return jsonify({'message':'No bookmarks available'}),404
    for book1 in bookmk:
        db.session.delete(book1)
        db.session.commit()
    return jsonify({'message':'bookmarks is deleted'}),202

@book.delete('/delete/<string:short_url>')
@jwt_required()
@swag_from('docs/bookmark/delete_short_url.yml')
def book_delete1(short_url):
    book=bookmark.query.filter_by(short_url=short_url).first()
    if not book:
        return jsonify({'message':'short_url is not in your bookmarks'}),404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message':'bookmark is deleted'}),202

@book.get('/list/stat')
@jwt_required()
@swag_from('docs/bookmark/stat.yml')
def stats():
    user_id=get_jwt_identity()
    bookmk=bookmark.query.filter_by(user_id=user_id).all()
    if not bookmk:
        return jsonify({'message':'No bookmarks available'}),404
    l={}
    for i in range(len(bookmk)):
        l[str(i+1)]={}
        l[str(i+1)]['short_url']=bookmk[i].short_url
        l[str(i+1)]['url']=bookmk[i].url
        l[str(i+1)]['views']=bookmk[i].views

    return jsonify(l),200

