from flask import Blueprint, request, jsonify
from app.models.meal import Meal, FoodInMeal
from app.models.food import Food
from app.database import db
from datetime import datetime

meal_bp = Blueprint('meal', __name__)

'''---Rota para registrar refeição---'''
@meal_bp.route('/meal', methods=['POST'])
def create_meal():
    data = request.get_json()
    user_id = data.get('user_id')
    foods = data.get('foods', [])
    total_calories = data.get('total_calories')
    date_str = data.get('date')

    # Validar dados da refeição
    if not user_id or not foods or total_calories is None:
        return jsonify({'error': 'User ID, foods, and total calories are required'}), 400

    # Validar data
    if not date_str:
        date_str = datetime.utcnow().isoformat()

    # Converter a string para datetime
    try:
        meal_date = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Criar a refeição
    meal = Meal(user_id=user_id, total_calories=total_calories, date=meal_date)
    db.session.add(meal)

    # Adicionar alimentos na refeição
    for food in foods:
        food_id = food.get('food_id')
        quantity = food.get('quantity')
        calories = food.get('calories')

        # Validar dados dos alimentos
        if not food_id or quantity is None or calories is None:
            return jsonify({'error': 'Food ID, quantity, and calories are required'}), 400

        # Verificar se o alimento existe
        linked_food = Food.query.get(food_id)
        if not linked_food:
            return jsonify({'error': f'Food with ID {food_id} not found'}), 404

        # Adicionar o alimento na refeição
        food_in_meal = FoodInMeal(
            meal_id=meal.id,
            food_id=food_id,
            quantity=quantity,
            calories=calories,
        )
        meal.foods.append(food_in_meal)

    # Salvar a refeição
    db.session.commit()
    meal.update_user_calories()

    return jsonify(meal.to_dict()), 201



'''---Rota para obter refeição---'''
@meal_bp.route('/meals', methods=['GET'])
def get_meals():
    user_id = request.args.get('user_id')

    # Verificar se o ID do usuário foi fornecido
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Buscar os registros de refeição
    meals = Meal.query.filter_by(user_id=user_id).all()

    # Verificar se refeição foi encontrada
    if not meals:
        return jsonify({'message': 'No meals found for this user'}), 404

    # Buscar os alimentos associados a cada refeição
    meals_with_foods = []
    for meal in meals:
        meal_dict = meal.to_dict()
        foods_in_meal = []

        for food_in_meal in meal.foods:
            if food_in_meal.food:
                foods_in_meal.append({
                    'food': food_in_meal.food.name,
                    'calories': food_in_meal.calories,
                    'quantity': food_in_meal.quantity,
                    'time': meal.date,
                })

        # Adicionar alimentos associados a cada refeição
        meal_dict['foods'] = foods_in_meal
        meals_with_foods.append(meal_dict)

    return jsonify(meals_with_foods), 200