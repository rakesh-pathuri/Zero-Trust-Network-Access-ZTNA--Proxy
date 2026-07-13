from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def internal_resource(path):
    """
    A dummy backend application that simulates an internal company resource.
    It should never be exposed directly to the internet; it only accepts traffic from the ZTNA proxy.
    """
    return jsonify({
        "status": "success",
        "message": "You have successfully accessed the protected internal resource.",
        "requested_path": f"/{path}",
        "security_level": "Classified"
    }), 200

if __name__ == '__main__':
    print("Starting Hidden Internal Application on port 8000...")
    # Bind only to localhost to simulate internal network isolation
    app.run(host='127.0.0.1', port=8000, debug=True)
