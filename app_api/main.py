from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded username and password (for demo purposes)
valid_username = "user"
valid_password = "password"

@app.route('/login', methods=['POST'])
def login():
    # Get the JSON data from the request
    data = request.get_json()

    # Check if both username and password are provided
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Both username and password are required."}), 400

    # Get username and password from the JSON data
    username = data['username']
    password = data['password']

    # Compare provided credentials with the hardcoded values
    if username == valid_username and password == valid_password:
        return jsonify({"success": True, "message": "Login successful."}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

if __name__ == '__main__':
    app.run(debug=True)
