from flask import Flask, request, jsonify
import mysql.connector
import datetime
from datetime import datetime
from sql_creds import Credentials
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/get-team/<team_name>", methods=["GET"])
def get_Team_Name(team_name):
    cbb_betting_lines = mysql.connector.connect(
    host =  (Credentials.host).value,
    user =  (Credentials.user).value,
    password = (Credentials.password).value,
    database = (Credentials.database.value),
    )
    cursor = cbb_betting_lines.cursor()
    selectStatement = ("SELECT * FROM moneyline WHERE home = '%s' OR away = '%s'" % (team_name, team_name))
    cursor.execute(selectStatement)
    ans = cursor.fetchall()
    return jsonify(json.dumps(ans)), 200
    



@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    print(jsonify(data))
    return jsonify(data), 201


if __name__ == "__main__":
    app.run(debug=True)