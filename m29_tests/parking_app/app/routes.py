# app/routes.py

from flask import Blueprint, request, jsonify
from .models import Client, Parking, ClientParking
from . import db
from datetime import datetime

bp = Blueprint('main', __name__)

# GET /clients
@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'surname': c.surname,
        'car_number': c.car_number
    } for c in clients]), 200

# GET /clients/<id>
@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'surname': client.surname,
        'car_number': client.car_number
    }), 200

# POST /clients
@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'id': client.id}), 201

# POST /parkings
@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.json
    parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=data['count_places'],
        count_available_places=data['count_places']
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify({'id': parking.id}), 201

# POST /client_parkings — заезд
@bp.route('/client_parkings', methods=['POST'])
def park_car():
    data = request.json
    client = Client.query.get(data['client_id'])
    parking = Parking.query.get(data['parking_id'])

    if not client or not parking:
        return jsonify({'error': 'Client or Parking not found'}), 404

    if not parking.opened:
        return jsonify({'error': 'Parking is closed'}), 400

    if parking.count_available_places <= 0:
        return jsonify({'error': 'No available spots'}), 400

    if not client.credit_card:
        return jsonify({'error': 'Client has no credit card'}), 400

    parking.count_available_places -= 1
    cp = ClientParking(client_id=client.id, parking_id=parking.id)
    db.session.add(cp)
    db.session.commit()
    return jsonify({'message': 'Car parked'}), 200

# DELETE /client_parkings — выезд
@bp.route('/client_parkings', methods=['DELETE'])
def unpark_car():
    data = request.json
    client_id = data['client_id']
    parking_id = data['parking_id']
    cp = ClientParking.query.filter_by(client_id=client_id, parking_id=parking_id, time_out=None).first()

    if not cp:
        return jsonify({'error': 'Entry not found'}), 404

    cp.time_out = datetime.utcnow()

    if cp.time_out < cp.time_in:
        return jsonify({'error': 'Invalid time range'}), 400

    parking = Parking.query.get(parking_id)
    parking.count_available_places += 1

    db.session.commit()
    return jsonify({'message': 'Car left, payment complete'}), 200