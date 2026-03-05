from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Temporary storage (replace later with database)
students = []

@app.route("/")
def home():
    return render_template("app.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    sapid = request.form.get("sapid")
    age = request.form.get("age")
    marks = request.form.get("marks")

    student = {
        "name": name,
        "sapid": sapid,
        "age": age,
        "marks": marks
    }

    students.append(student)

    return jsonify({
        "message": "Student data received",
        "data": student
    })


@app.route("/students")
def get_students():
    return jsonify(students)


if __name__ == "__main__":
    app.run(debug=True)