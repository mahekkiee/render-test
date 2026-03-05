from flask import Flask, request, send_from_directory, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


@app.route("/")
def home():
    return send_from_directory(".", "app.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    sapid = request.form.get("sapid")
    age = request.form.get("age")
    marks = request.form.get("marks")

    cursor.execute(
        "INSERT INTO students (name, sapid, age, marks) VALUES (%s,%s,%s,%s)",
        (name, sapid, age, marks)
    )

    conn.commit()

    return "Student stored successfully"


@app.route("/students")
def get_students():

    cursor.execute("SELECT name FROM students")
    rows = cursor.fetchall()

    names = [r[0] for r in rows]

    return jsonify(names)


@app.route("/student/<name>")
def get_student(name):

    cursor.execute(
        "SELECT name, sapid, age, marks FROM students WHERE name=%s",
        (name,)
    )

    row = cursor.fetchone()

    if row:
        return jsonify({
            "name": row[0],
            "sapid": row[1],
            "age": row[2],
            "marks": row[3]
        })

    return jsonify({"error": "student not found"})
