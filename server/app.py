#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        new_user={}
        json = request.get_json()
        user = User(
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

        new_user = {
            "id" : user.id,
            "username" : user.username
        } 

        return new_user, 201

class CheckSession(Resource):
    def get(self):

        user=User.query.filter(User.id == session.get('user_id')).first()
        
        if user:
            print ("this is user", user)
            return (
             {
                "id" : user.id,
                "username" : user.username
             } 
            ),201
        else:
            return {}, 204
  
class Login(Resource):
    def post(self):

        username = request.get_json()['username']
        user = User.query.filter(User.username == username).first()
        
        #get password
        password = request.get_json()['password']

        # if the password authenticates then set the session
        # with the user's id
        if user.authenticate(password):
            session['user_id'] = user.id
            return (
             {
                "id" : user.id,
                "username" : user.username
             } 
            ),201
        return {'error': 'Invalid username or password'}, 401   

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204
    
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession,'/check_session', endpoint='check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
