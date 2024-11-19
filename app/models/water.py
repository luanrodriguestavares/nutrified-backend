from app.database import db
from app.models.user import User
from datetime import datetime

'''---Modelo para registros de água---'''
class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='water_entries', lazy=True)

    # Converte o objeto para um dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quantity": self.quantity,
            "date": self.date.isoformat()
        }
    
    # Atualiza a quantidade de água consumida pelo usuário  
    def update_user_water(self):
        user = User.query.get(self.user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        if not hasattr(user, 'daily_water_consumed'):
            raise AttributeError("O modelo User precisa do atributo 'daily_water_consumed'")
        
        user.daily_water_consumed = (user.daily_water_consumed or 0) + self.quantity
        
        db.session.commit()
