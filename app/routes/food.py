from flask import Blueprint, request, jsonify
from app.models.food import Food
from app.database import db

food_bp = Blueprint('food', __name__)

'''---Rota para registrar alimentos---'''
@food_bp.route('/', methods=['POST'])
def create_food():
    data = request.get_json()
    name = data.get('name')
    calories_per_portion = data.get('calories_per_portion')

    # Verificar se os campos obrigatórios estão presentes
    if not name or not calories_per_portion:
        return jsonify({'error': 'Name and calories per portion are required'}), 400

    # Criar o novo alimento
    food = Food(name=name, calories_per_portion=calories_per_portion)
    db.session.add(food)
    db.session.commit()

    return jsonify(food.to_dict()), 201



'''---Rota para listar alimentos---'''
@food_bp.route('/', methods=['GET'])
def list_foods():
    foods = Food.query.all()
    return jsonify([food.to_dict() for food in foods]), 200



'''---Rota para buscar alimentos com filtro---'''
@food_bp.route('/', methods=['GET'])
def get_foods():
    search = request.args.get('search', '')
    limit = request.args.get('limit', 10, type=int)
    
    # Buscar alimentos com base no filtro
    foods = Food.query.filter(Food.name.ilike(f'%{search}%')).limit(limit).all()
    
    return jsonify([food.to_dict() for food in foods]), 200