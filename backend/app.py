# backend/app.py
from flask import Flask, request, jsonify
import redis
import os
from datetime import datetime

app = Flask(__name__)

# Connect to Redis (Docker container name)
redis_client = redis.Redis(host='redis-db', port=6379, decode_responses=True)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = redis_client.get('users')
    if users:
        return jsonify({'users': eval(users)})
    return jsonify({'users': []})

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    users = eval(redis_client.get('users') or '[]')
    user = {
        'name': data.get('name', 'Anonymous'),
        'id': len(users) + 1,
        'timestamp': datetime.now().isoformat()
    }
    users.append(user)
    redis_client.set('users', str(users))
    return jsonify({'success': True, 'user': user})

@app.route('/health')
def health():
    return {'status': 'healthy', 'redis': redis_client.ping()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
