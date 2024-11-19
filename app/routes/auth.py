from flask import Blueprint, request, jsonify, make_response, session
from werkzeug.security import check_password_hash
from app.models.user import User
from app.services.user_service import UserService
from app.database import db

auth_bp = Blueprint('auth', __name__)

'''Rota de Registro de Usuário'''
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Verificar se os campos obrigatórios estão presentes
    required_fields = ['username', 'email', 'password', 'age', 'height', 'weight', 'goal', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields', 'data': data}), 400

    # Verificar se o username ou email já existem
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    # Criar o novo usuário
    user = User(
        username=data['username'],
        email=data['email'],
        age=data['age'],
        height=data['height'],
        weight=data['weight'],
        goal=data['goal'],
        gender=data['gender']
    )
    user.set_password(data['password'])

    # Calcular calorias e água
    user.calories = UserService.calculate_calories(user)
    user.water = UserService.calculate_water(user)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201



'''---Rota de Login de Usuário---''' 
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    # Verificar se o email foi encontrado
    if not user:
        return jsonify({'error': 'Email not found'}), 404
    
    # Verificar se a senha esta correta
    if not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Incorrect password'}), 401

    # Logar o usuário e definir o cookie
    response = make_response(jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200)
    response.set_cookie('user_id', str(user.id), max_age=60*60*24, httponly=True, secure=True)
    response.headers['Access-Control-Allow-Credentials'] = 'true'  
    return response



'''---Rota de Logout de Usuário---'''
@auth_bp.route('/logout', methods=['POST'])
def logout():
    
    # Remover o cookie e limpar a sessão
    session.pop('user_id', None) 
    response = jsonify({"message": "Logout bem-sucedido"})
    response.delete_cookie('user_id')
    return response, 200



'''---Rota de Autenticação de Usuário---'''
@auth_bp.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')

    # Verificar se o usuário está logado
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    user = User.query.get(user_id)
    
    # Verificar se o usuário foi encontrado
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200