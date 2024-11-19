from flask import Flask
from flask_cors import CORS
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.food import food_bp 
from app.routes.meal import meal_bp
from app.routes.water import water_bp
from app.database import db
from app.scripts.seed_food import seed_foods

CORS(auth_bp, supports_credentials=True)

# Função para criar o aplicativo
def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

    # Configurando o banco de dados
    app.config['SECRET_KEY'] = 'nutrified_ap3_lab'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Cria as tabelas no banco de dados
    with app.app_context():
        db.create_all()  
        seed_foods()

    # Registra as rotas
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(food_bp, url_prefix='/food') 
    app.register_blueprint(meal_bp, url_prefix='/meal') 
    app.register_blueprint(water_bp, url_prefix='/water')

    return app
