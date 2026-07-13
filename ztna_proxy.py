import os
import jwt
import requests
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET_KEY", "fallback_insecure_key")
INTERNAL_APP_URL = os.getenv("INTERNAL_APP_URL", "http://localhost:8000")

app = Flask(__name__)

def verify_token(auth_header):
    """
    Cryptographically verifies the JWT signature and expiration.
    Returns the decoded payload if valid, or an error message if invalid.
    """
    if not auth_header or not auth_header.startswith("Bearer "):
        return False, "Missing or malformed Authorization header"

    token = auth_header.split(" ")[1]

    try:
        # jwt.decode automatically verifies the signature and the 'exp' claim
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return True, decoded_payload
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid cryptographic token"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def zero_trust_proxy(path):
    """
    The main ZTNA Proxy interceptor.
    Every single request must pass cryptographic verification before being routed.
    """
    auth_header = request.headers.get("Authorization")
    
    is_valid, result = verify_token(auth_header)
    if not is_valid:
        # Block access completely at the network edge
        return jsonify({"error": "Zero-Trust Policy Violation", "details": result}), 401

    # Extract user identity for logging/auditing
    user_identity = result.get("sub")
    print(f"[AUDIT] Authorized access granted to user: {user_identity} for path: /{path}")

    # Route the request to the hidden internal application
    target_url = f"{INTERNAL_APP_URL}/{path}"
    
    try:
        # Proxy the request forward
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        # Return the internal app's response back to the client
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Internal Application Unreachable"}), 502

if __name__ == '__main__':
    print("Starting Zero-Trust Identity Proxy on port 5000...")
    app.run(port=5000, debug=True)
