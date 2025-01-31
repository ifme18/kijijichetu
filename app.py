import os
from flask import Flask, request, jsonify
from models import db, Community, User,Event, Estate,Notification
from models import db, Community, User, Event, Estate, Notification
from datetime import datetime
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Community API!"


@app.route('/communities', methods=['GET'])
def get_communities():
    communities = Community.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'location': c.location
    } for c in communities])

@app.route('/communities/<int:id>', methods=['GET'])
def get_community(id):
    community = Community.query.get_or_404(id)
    return jsonify({
        'id': community.id,
        'name': community.name,
        'location': community.location
    })
@app.route('/communities/<int:id>', methods=['DELETE'])
def delete_community(id):
    community = Community.query.get_or_404(id)
    db.session.delete(community)
    db.session.commit()
    return jsonify({'message': 'Community deleted successfully'}), 200

@app.route('/communities/<int:id>', methods=['PUT'])
def update_community(id):
    community = Community.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        community.name = data['name']
    if 'location' in data:
        community.location = data['location']

    db.session.commit()

    return jsonify({
        'id': community.id,
        'name': community.name,
        'location': community.location,
        'message': 'Community updated successfully'
    })

@app.route('/communities', methods=['POST'])
def create_community():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    
    if 'name' not in data or 'location' not in data:
        return jsonify({"error": "name and location are required"}), 400
        
    community = Community(
        name=data['name'],
        location=data['location']
    )
    
    db.session.add(community)
    db.session.commit()
    
    return jsonify({
        'id': community.id,
        'name': community.name,
        'location': community.location
    }), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'occupation': u.occupation,
        'phoneno': u.phoneno,
        'houseno': u.houseno,
        'community_id': u.community_id
    } for u in users])
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_users(id):
    users = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user deleted successfully'}), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'occupation': user.occupation,
        'phoneno': user.phoneno,
        'houseno': user.houseno,
        'community_id': user.community_id
    })

@app.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    required_fields = ['name', 'email', 'community_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "name, email, and community_id are required"}), 400
    
    user = User(
        name=data['name'],
        email=data['email'],
        occupation=data.get('occupation'),
        phoneno=data.get('phoneno'),
        houseno=data.get('houseno'),
        community_id=data['community_id']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'community_id': user.community_id
    }), 201


@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id,
        'eventname': e.eventname,
        'eventdate': e.eventdate.isoformat(),
        'community_id': e.community_id
    } for e in events])

@app.route('/events', methods=['POST'])
def create_event():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    required_fields = ['eventname', 'eventdate', 'community_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "eventname, eventdate, and community_id are required"}), 400
    
    try:
        eventdate = datetime.fromisoformat(data['eventdate'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format (e.g., 2025-01-29T15:30:00Z)"}), 400
    
    event = Event(
        eventname=data['eventname'],
        eventdate=eventdate,
        community_id=data['community_id']
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'id': event.id,
        'eventname': event.eventname,
        'eventdate': event.eventdate.isoformat(),
        'community_id': event.community_id
    }), 201


@app.route('/estates', methods=['GET'])
def get_estates():
    estates = Estate.query.all()
    return jsonify([{
        'id': e.id,
        'estatename': e.estatename,
        'user_id': e.user_id,
        'community_id': e.community_id
    } for e in estates])

@app.route('/estates', methods=['POST'])
def create_estate():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    required_fields = ['estatename', 'user_id', 'community_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "estatename, user_id, and community_id are required"}), 400
    
    estate = Estate(
        estatename=data['estatename'],
        user_id=data['user_id'],
        community_id=data['community_id']
    )
    
    db.session.add(estate)
    db.session.commit()
    
    return jsonify({
        'id': estate.id,
        'estatename': estate.estatename,
        'user_id': estate.user_id,
        'community_id': estate.community_id
    }), 201


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)