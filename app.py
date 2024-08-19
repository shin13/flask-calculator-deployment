from flask import Flask, render_template, request, g, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "medicines.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    db = get_db()
    cur = db.execute("SELECT * FROM medicines")
    medicines = cur.fetchall()

    return render_template("calculator.html", medicines=medicines)


@app.route("/calculate", methods=["POST"])
def calculate():
    weight = float(request.json["weight"])
    results = {}

    db = get_db()
    cur = db.execute("SELECT * FROM medicines")
    medicines = cur.fetchall()

    for medicine in medicines:
        # Check if max_ml_per_kg_day is not None before doing the multiplication
        if medicine["max_ml_per_kg_day"] is not None:
            daily_max_ml = min(
                weight * medicine["max_ml_per_kg_day"], medicine["max_daily_ml"]
            )
        else:
            daily_max_ml = medicine["max_daily_ml"]
        single_dose_min_ml = weight * medicine["lowest_ml_kg"]
        single_dose_max_ml = weight * medicine["highest_ml_kg"]

        results[medicine["drug_code"]] = {
            "daily_max_ml": round(daily_max_ml, 2),
            "single_dose_min_ml": round(single_dose_min_ml, 2),
            "single_dose_max_ml": round(single_dose_max_ml, 2),
        }

    return jsonify(results)


if __name__ == "__main__":
    app.run()
