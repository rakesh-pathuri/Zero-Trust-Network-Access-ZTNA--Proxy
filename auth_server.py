import os
import datetime
import jwt
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET_KEY", "fallback_insecure_key")

app = Flask(__name__)

# Mock Database for User Identities
USERS_DB = {
    "admin": "admin_secure_password",
    "operator": "operator_123"
}

@app.route('/login', methods=['POST'])
def login():
    """
    Identity Provider (IdP) endpoint. 
    Validates credentials and mints a cryptographically signed JWT.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if USERS_DB.get(username) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate the JSON Web Token (JWT)
    # The payload contains the identity claim and a strict expiration timestamp
    payload = {
        "sub": username,
        "role": "admin" if username == "admin" else "user",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15) # 15 min TTL
    }

    # Sign the token symmetrically using HS256 and the secret key
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "message": "Authentication successful",
        "token": token
    }), 200

if __name__ == '__main__':
    print("Starting Auth Server on port 5001...")
    app.run(port=5001, debug=True)
