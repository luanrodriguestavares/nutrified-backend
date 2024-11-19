from flask import Blueprint, jsonify
from app.models.user import User
from app.models.meal import Meal
from app.services.user_service import UserService
from app.database import db  

user_bp = Blueprint('user', __name__)

'''---Rota para obter um usuário pelo ID---'''
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    # Verificar se o usuário foi encontrado
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200



'''---Rota para obter as necessidades do usuário---'''
@user_bp.route('/<int:user_id>/needs', methods=['GET'])
def get_user_needs(user_id):
    user = User.query.get(user_id)

    # Verificar se o usuário foi encontrado
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Calcular as necessidades do usuário
    calories = UserService.calculate_calories(user)
    water = UserService.calculate_water(user)

    # Retornar as necessidades
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'calories_needed': calories,
        'calories_consumed': user.daily_calories_consumed,
        'last_meal_date': user.last_meal_date,
        'last_water_date': user.last_water_date,
        'water_consumed': user.daily_water_consumed,
        'water_needed': water
    }), 200



'''---Rota para atualizar as calorias diarias do usuário---'''
@user_bp.route('/<int:user_id>/update_daily_calories', methods=['POST'])
def update_daily_calories(user_id):
    user = User.query.get(user_id)

    # Verificar se o usuário foi encontrado
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Atualizar as calorias diarias
    meals = Meal.query.filter_by(user_id=user_id).all()  
    daily_calories = sum(meal.total_calories for meal in meals) 

    # Atualizar as calorias diarias
    user.daily_calories_consumed = daily_calories
    db.session.commit()

    # Retornar uma mensagem de sucesso
    return jsonify({'message': 'Daily calories updated successfully'}), 200
