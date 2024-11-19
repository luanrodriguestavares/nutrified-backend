from app.database import db

'''---Modelo para alimentos---'''
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    calories_per_portion = db.Column(db.Float, nullable=False)
    portion_weight = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    # Converte o objeto para um dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "calories_per_portion": self.calories_per_portion,
            "portion_weight": self.portion_weight,
            "category": self.category
        }