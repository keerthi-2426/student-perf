import pandas as pd
from backend.app import app, db
from backend.models import Student, Score, Attendance

# Load CSV
df = pd.read_csv("data/students.csv")

with app.app_context():
    for _, row in df.iterrows():
        # Create student
        student = Student(
            name=row["name"],
            age=row["age"],
            gender=row["gender"],
            socio_economic=row["socio_economic"]
        )
        db.session.add(student)
        db.session.flush()  # get student.id before commit

        # Add score
        score = Score(
            student_id=student.id,
            term=row["term"],
            test_score=row["test_score"],
            exam_score=row["exam_score"],
            coursework_score=row["coursework_score"]
        )
        db.session.add(score)

        # Add attendance
        attendance = Attendance(
            student_id=student.id,
            term=row["term"],
            present_days=row["present_days"],
            total_days=row["total_days"]
        )
        db.session.add(attendance)

    db.session.commit()
    print("✅ Data imported successfully!")