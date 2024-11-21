from app.database import db
from app.models.user import User
from app.models.food import Food
from sqlalchemy.orm import validates
from datetime import datetime

'''---Modelo para refeição---'''
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_calories = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    foods = db.relationship('FoodInMeal', backref='meal', lazy=True)

    # Valida o total de calorias
    @validates('total_calories')
    def validate_total_calories(self, key, value):
        if value < 0:
            raise ValueError("Total calories must be a positive value")
        return value

    # Converte o objeto para um dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_calories': self.total_calories,
            'date': self.date.isoformat(),
            'foods': [
                food.to_dict() for food in self.foods if food.food is not None
            ], 
        }

    # Atualiza a quantidade de calorias consumidas pelo usuário
    def update_user_calories(self):
        user = User.query.get(self.user_id)
        if user:
            user.reset_daily_calories()
            user.daily_calories_consumed += self.total_calories
            db.session.commit()



'''---Modelo para comida em uma refeição---'''
class FoodInMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    food = db.relationship('Food', backref='food_in_meals', lazy=True)

    # Converte o objeto para um dicionário
    def to_dict(self):
        return {
            'food_id': self.food_id,
            'food_name': self.food.name if self.food else 'Unknown',
            'quantity': self.quantity,
            'calories': self.calories,
        }

    # Calcula as calorias totais dessa comida em uma refeição
    def calculate_total_calories(self):
        return self.quantity * self.calories