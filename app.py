from flask import Flask, request, send_from_directory, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return send_from_directory(".", "app.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        sapid = request.form.get("sapid")
        age = request.form.get("age")
        marks = request.form.get("marks")

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO students (name, sapid, age, marks) VALUES (%s,%s,%s,%s)",
            (name, sapid, age, marks)
        )

        conn.commit()
        cur.close()
        conn.close()

        return "Student stored successfully"

    except Exception as e:
        return str(e)


@app.route("/search")
def search():
    name = request.args.get("name")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT name,sapid,age,marks FROM students WHERE LOWER(name) LIKE LOWER(%s)",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "sapid": r[1],
            "age": r[2],
            "marks": r[3]
        })

    return jsonify(data)


if __name__ == "__main__":
    app.run()
