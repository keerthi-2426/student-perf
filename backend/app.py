from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)

# CSV file
csv_file = os.path.join(os.path.dirname(__file__), "students.csv")

# Helper: load students
def load_students():
    students = []
    if os.path.exists(csv_file):
        with open(csv_file, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "test_score": float(row["test_score"]),
                    "attendance": float(row["attendance"]),
                    "prediction": float(row["prediction"]),
                    "accuracy": float(row.get("accuracy", 0)),
                    "performance": row.get("performance", "")
                })
    return students

# Save students
def save_students(students):
    with open(csv_file, "w", newline='') as f:
        fieldnames = ["id", "name", "test_score", "attendance", "prediction", "accuracy", "performance"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in students:
            writer.writerow(s)

# Performance calculation
def get_performance(test_score, attendance):
    if test_score < 40 or attendance < 40:
        return "Poor Performance ⚠️"
    avg = (test_score + attendance) / 2
    if avg < 60:
        return "Average Performance"
    elif avg < 80:
        return "Good Performance"
    else:
        return "Excellent Performance 🎉"

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Add & predict
@app.route('/predict', methods=['POST'])
def predict():
    students = load_students()
    name = request.form['name']
    test_score = float(request.form['test_score'])
    attendance = float(request.form['attendance'])

    prediction = (test_score + attendance) / 2
    accuracy = prediction
    performance = get_performance(test_score, attendance)

    students.append({
        "id": len(students) + 1,
        "name": name,
        "test_score": test_score,
        "attendance": attendance,
        "prediction": prediction,
        "accuracy": accuracy,
        "performance": performance
    })

    save_students(students)
    return redirect(url_for('dashboard'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    students = load_students()
    return render_template('dashboard.html', students=students)

# Delete
@app.route('/delete/<int:student_id>')
def delete(student_id):
    students = load_students()
    students = [s for s in students if s["id"] != student_id]
    for i, s in enumerate(students):
        s["id"] = i + 1
    save_students(students)
    return redirect(url_for('dashboard'))

# Edit
@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)
    if request.method == 'POST':
        student["name"] = request.form['name']
        student["test_score"] = float(request.form['test_score'])
        student["attendance"] = float(request.form['attendance'])
        student["prediction"] = (student["test_score"] + student["attendance"]) / 2
        student["accuracy"] = student["prediction"]
        student["performance"] = get_performance(student["test_score"], student["attendance"])
        save_students(students)
        return redirect(url_for('dashboard'))
    return render_template('edit.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)
