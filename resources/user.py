import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('user', 'user')

@user.route('/register', methods=['POST']) #
def register():
	payload = request.get_json()
	print(payload)

	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		models.User.get(models.User.email == payload['email'])
		return jsonify (
			data={},
			message="a user with that email already exists", 
			status=401
			), 401
	except models.DoesNotExist:
		created_user = models.User.create(
			username=payload['username'],
			email=payload['email'],
			password=generate_password_hash(payload['password'])
			)
		login_user(created_user)
		user_dict = model_to_dict(created_user)
		print(user_dict)
		print(type(user_dict['password']))
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"successfully registered as {user_dict['email']}", 
			status=201
			), 201
			

# USERS:
# 		POST '/register' <<--allows users to instatiate themeselves in the app
# 		POST '/login' <<--takes credentials to use app	
# 		GET '/logged_in' <<--tracks current user
# 		GET '/logout' <<--allows session to end	