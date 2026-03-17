from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

# ---------------- CONFIG ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"
DATA_FILE = "data.json"

# ---------------- LOGIN PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Wrong username or password")

    return render_template("login.html")


# ---------------- DASHBOARD PAGE ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    else:
        data = {
            "cars": 0,
            "bikes": 0,
            "bus": 0,
            "truck": 0,
            "total": 0,
            "capacity": 50,
            "status": "PARKING AVAILABLE"
        }

    return render_template("dashboard.html", data=data)


# ---------------- API FOR LIVE DATA ----------------
@app.route("/api/data")
def api_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    else:
        data = {
            "cars": 0,
            "bikes": 0,
            "bus": 0,
            "truck": 0,
            "total": 0,
            "capacity": 50,
            "status": "PARKING AVAILABLE"
        }

    return jsonify(data)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
