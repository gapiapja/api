from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# File untuk menyimpan data
USERS_FILE = 'users_data.json'

def load_data():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

def save_data(data):
    with open(USERS_FILE, 'w') as file:
        json.dump(data, file, indent=2)

# Root endpoint untuk informasi API
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Selamat datang di User Management API",
        "endpoints": {
            "register": "/register (POST)",
            "login": "/login (POST)",
            "get_users": "/users (GET)",
            "update_password": "/users/update_password (PUT)",
            "delete_user": "/users/delete (DELETE)"
        }
    })

# Endpoint untuk registrasi user baru
@app.route('/register', methods=['POST'])
def register():
    data = load_data()
    
    if not request.is_json:
        return jsonify({"message": "Format harus JSON!"}), 400
    
    content = request.get_json()
    username = content.get('username')
    password = content.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username dan password harus diisi!"}), 400
    
    if username in data['users']:
        return jsonify({"message": "Username sudah terdaftar!"}), 400
    
    data['users'][username] = {
        "password": password,
        "created_at": datetime.now().isoformat()
    }
    
    save_data(data)
    return jsonify({
        "message": "Registrasi berhasil!", 
        "data": {
            "username": username,
            "created_at": data['users'][username]['created_at']
        }
    }), 201

# Endpoint untuk login
@app.route('/login', methods=['POST'])
def login():
    data = load_data()
    
    if not request.is_json:
        return jsonify({"message": "Format harus JSON!"}), 400
    
    content = request.get_json()
    username = content.get('username')
    password = content.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username dan password harus diisi!"}), 400
    
    if username not in data['users'] or data['users'][username]['password'] != password:
        return jsonify({"message": "Username atau password salah!"}), 401
    
    return jsonify({
        "message": "Login berhasil!",
        "data": {
            "username": username,
            "login_time": datetime.now().isoformat()
        }
    })

# Endpoint untuk mendapatkan semua user
@app.route('/users', methods=['GET'])
def get_users():
    data = load_data()
    users_list = []
    for username, user_data in data['users'].items():
        users_list.append({
            "username": username,
            "created_at": user_data['created_at']
        })
    return jsonify({
        "total_users": len(users_list),
        "users": users_list
    })

# Endpoint untuk update password
@app.route('/users/update_password', methods=['PUT'])
def update_password():
    data = load_data()
    
    if not request.is_json:
        return jsonify({"message": "Format harus JSON!"}), 400
    
    content = request.get_json()
    username = content.get('username')
    old_password = content.get('old_password')
    new_password = content.get('new_password')
    
    if not all([username, old_password, new_password]):
        return jsonify({"message": "Semua field harus diisi!"}), 400
    
    if username not in data['users']:
        return jsonify({"message": "User tidak ditemukan!"}), 404
    
    if data['users'][username]['password'] != old_password:
        return jsonify({"message": "Password lama salah!"}), 401
    
    data['users'][username]['password'] = new_password
    data['users'][username]['updated_at'] = datetime.now().isoformat()
    save_data(data)
    
    return jsonify({
        "message": "Password berhasil diupdate!",
        "data": {
            "username": username,
            "updated_at": data['users'][username]['updated_at']
        }
    })

# Endpoint untuk hapus user
@app.route('/users/delete', methods=['DELETE'])
def delete_user():
    data = load_data()
    
    if not request.is_json:
        return jsonify({"message": "Format harus JSON!"}), 400
    
    content = request.get_json()
    username = content.get('username')
    password = content.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username dan password harus diisi!"}), 400
    
    if username not in data['users']:
        return jsonify({"message": "User tidak ditemukan!"}), 404
    
    if data['users'][username]['password'] != password:
        return jsonify({"message": "Password salah!"}), 401
    
    del data['users'][username]
    save_data(data)
    
    return jsonify({
        "message": "User berhasil dihapus!",
        "data": {
            "username": username,
            "deleted_at": datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    print("Server berjalan")
    app.run(host='0.0.0.0')