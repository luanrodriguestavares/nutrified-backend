from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.water import Water
from app.database import db
from datetime import datetime

water_bp = Blueprint('water', __name__)

'''---Rota para registrar um registro de água---'''
@water_bp.route('/record', methods=['POST'])
def add_water_record():
    data = request.get_json()
    user_id = data.get('user_id')
    quantity = data.get('quantity')

    # Verificar se os campos obrigatórios estão presentes
    if not user_id or quantity is None:
        return jsonify({'error': 'User ID and quantity are required'}), 400

    # Verificar se a quantidade de água é maior que 0
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be greater than 0'}), 400

    # Criar o registro de água
    water = Water(user_id=user_id, quantity=quantity)
    db.session.add(water)
    db.session.commit()  

    # Atualizar a quantidade de água consumida pelo usuário
    try:
        water.update_user_water()
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except AttributeError as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(water.to_dict()), 201



'''---Rota para obter os registros de água---'''
@water_bp.route('/logs', methods=['GET'])
def get_water():
    user_id = request.args.get('user_id')

    # Verificar se o ID do usuário foi fornecido
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Buscar os registros de água
    logs = Water.query.filter_by(user_id=user_id).all()
    if not logs:
        return jsonify({'message': 'No water logs found for this user'}), 404

    return jsonify([log.to_dict() for log in logs]), 200
