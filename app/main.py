"""
Simple user management microservice with intentional security issues
"""
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def validate_email(email):
    """
    Email validation function with a subtle bug
    Bug: allows emails without @ symbol if they contain a dot
    """
    if '.' in email:  # BUG: Missing @ validation
        return True
    return False

def get_db_connection():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "user-management"}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    email = data.get('email', '')
    username = data.get('username', '')
    
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    
    # Simulate user creation
    return jsonify({
        "message": "User created successfully",
        "email": email,
        "username": username
    }), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # Vulnerable SQL query (for demonstration)
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection vulnerability
    
    return jsonify({"user_id": user_id, "status": "found"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
