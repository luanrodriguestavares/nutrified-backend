from flask import Blueprint, request, jsonify
from app.models.meal import Meal, FoodInMeal
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

    # Verificar se os campos obrigatórios estão presentes
    if not user_id or not foods or total_calories is None:
        return jsonify({'error': 'User ID, foods, total calories, and date are required'}), 400

    # Verificar se a data foi fornecida
    if not date_str:
        date_str = datetime.utcnow().isoformat()

    # Converter a data fornecida em um objeto datetime
    try:
        meal_date = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Criar a refeição
    meal = Meal(user_id=user_id, total_calories=total_calories, date=meal_date)
    db.session.add(meal)

    # Adicionar alimentos a refeição
    for food in foods:
        food_in_meal = FoodInMeal(
            meal_id=meal.id,
            food_id=food['food_id'],
            quantity=food['quantity'],
            calories=food['calories']
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

    # Buscar todas as refeções do usuário
    meals = Meal.query.filter_by(user_id=user_id).all()

    # Verificar se refeções foram encontradas
    if not meals:
        return jsonify({'message': 'No meals found for this user'}), 404

    # Para cada refeição, incluir os alimentos detalhados
    meals_with_foods = []
    for meal in meals:
        meal_dict = meal.to_dict()
        foods_in_meal = []
        
        for food_in_meal in meal.foods:
            food = food_in_meal.food
            foods_in_meal.append({
                'food': food.name,  
                'calories': food_in_meal.calories,
                'quantity': food_in_meal.quantity,
                'time': meal.date, 
            })

        meal_dict['foods'] = foods_in_meal
        meals_with_foods.append(meal_dict)

    return jsonify(meals_with_foods), 200
