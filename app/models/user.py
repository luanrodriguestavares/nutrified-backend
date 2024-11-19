from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

'''---Modelo para Usuário---'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    goal = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    calories = db.Column(db.Float, nullable=True)
    water = db.Column(db.Float, nullable=True) 
    daily_calories_consumed = db.Column(db.Float, nullable=True, default=0) 
    last_meal_date = db.Column(db.Date, nullable=True)  
    daily_water_consumed = db.Column(db.Float, nullable=True, default=0) 
    last_water_date = db.Column(db.Date, nullable=True)

    # Função para criptografia de senha
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Função para verificação de senha
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Função para converter o objeto para um dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "goal": self.goal,
            "gender": self.gender,
            "calories": self.calories,
            "water": self.water,
            "daily_calories_consumed": self.daily_calories_consumed,
        }

    # Funções para resetar as calorias e o consumo diário de água
    def reset_daily_calories(self):
        today = datetime.utcnow().date()
        if self.last_meal_date != today:
            self.daily_calories_consumed = 0
            self.last_meal_date = today

    # Função para resetar o consumo diário de água
    def reset_daily_water(self):
        today = datetime.utcnow().date()
        if self.last_water_date != today:
            self.daily_water_consumed = 0
            self.last_water_date = today
