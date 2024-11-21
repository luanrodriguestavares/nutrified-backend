from flask import Blueprint, request, jsonify
from app.models.food import Food
from app.database import db

food_bp = Blueprint('food', __name__)

'''---Rota para registrar alimentos---'''
@food_bp.route('/', methods=['POST'])
def create_food():
    data = request.get_json()
    
    # Obtendo os dados enviados
    name = data.get('name')
    calories_per_portion = data.get('calories_per_portion')
    portion_weight = data.get('portion_weight')
    category = data.get('category')

    # Verificar se os campos obrigatórios estão presentes
    if not name or not calories_per_portion or not portion_weight or not category:
        return jsonify({'error': 'Name, calories per portion, portion weight and category are required'}), 400

    # Criar o novo alimento
    food = Food(
        name=name,
        calories_per_portion=calories_per_portion,
        portion_weight=portion_weight,
        category=category
    )
    
    db.session.add(food)
    db.session.commit()

    return jsonify(food.to_dict()), 201



'''---Rota para listar alimentos---'''
@food_bp.route('/', methods=['GET'])
def list_foods():
    foods = Food.query.all()
    return jsonify([food.to_dict() for food in foods]), 200