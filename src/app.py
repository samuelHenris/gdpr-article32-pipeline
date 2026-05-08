from flask import Flask, request, session, jsonify
import hashlib
import secrets
import logging
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

audit_log = []

class AuditLogger:
    @staticmethod
    def log_event(event_type, customer_id, action, ip_address):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "customer_id": customer_id,
            "action": action,
            "ip_address": ip_address,
            "processing_purpose": "CUSTOMER_AUTHENTICATION"
        }
        audit_log.append(entry)
        logging.info(json.dumps(entry))

class CustomerDatabase:
    def __init__(self):
        self.customers = {
            "test_user": {
                "id": "CUST-001",
                "password_hash": hashlib.pbkdf2_hmac('sha256', b"secure_password_123", b"salt", 100000).hex()
            }
        }
    
    def authenticate(self, password):
        provided_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), b"salt", 100000).hex()
        for username, data in self.customers.items():
            if data['password_hash'] == provided_hash:
                return {"customer_id": data['id'], "username": username}
        return None

db = CustomerDatabase()
audit = AuditLogger()

def require_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'customer_id' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"error": "Missing credentials"}), 400
    
    password = data.get('password')
    customer = db.authenticate(password)
    
    if customer:
        session['customer_id'] = customer['customer_id']
        session['username'] = customer['username']
        audit.log_event("LOGIN", customer['customer_id'], "authenticated", request.remote_addr)
        return jsonify({"status": "success", "customer_id": customer['customer_id']})
    
    audit.log_event("LOGIN_FAILED", "unknown", "failed_auth", request.remote_addr)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
@require_session
def logout():
    session.clear()
    return jsonify({"status": "logged_out"})

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "healthy", "service": "gdpr-article32-compliant"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
