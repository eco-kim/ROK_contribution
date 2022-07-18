from flask import Flask, request, jsonify

app = Flask(__name__)
app.id_count = 1
app.users = {}

@app.route("/sing-up", method=['POST'])
def sign_up():
    new_user = request.json
    new_user['id'] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1

    return jsonify(new_user)