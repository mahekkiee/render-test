from flask import Flask, request, send_from_directory

app = Flask(__name__)

students = []

@app.route("/")
def home():
    return send_from_directory(".", "app.html")

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

    return f"Data received: {student}"


if __name__ == "__main__":
    app.run(debug=True)
