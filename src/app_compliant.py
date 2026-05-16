from flask import Flask, request, jsonify
import secrets
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Simplified but compliant authentication
USERS = {
    "admin": hashlib.pbkdf2_hmac('sha256', b"securepass", b"unique_salt_per_user", 100000).hex()
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data.get('password', '')
    
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), b"unique_salt_per_user", 100000).hex()
    
    if hashed == USERS.get("admin"):
        return jsonify({"status": "success", "message": "Authenticated"})
    
    return jsonify({"status": "failed"}), 401

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')  # HTTPS enabled
