

from faker import Faker
import random
from .models import *
from django.db.models import Q, Sum

fake = Faker()

def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject = subject,
                    student = student,
                    marks = random.randint(0,100)
                )
    except Exception as e:
        print(e)

def seed_db(n=10) -> None:
    try:
        department_objs = list(Department.objects.all())
        print(f"Departments available: {len(department_objs)}")  # Debugging line

        # Check if departments exist
        if not department_objs:
            print("No departments found.")
            return

        for _ in range(n):
            # Ensure random_index is within the correct range
            if len(department_objs) > 0:
                random_index = random.randint(0, len(department_objs) - 1)
                department = department_objs[random_index]
            else:
                print("Error: No department to select from.")
                return

            student_id = f"STU-{random.randint(100, 999)}"
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(19, 30)
            student_address = fake.address()

            # Create StudentId object
            student_id_obj = StudentId.objects.create(student_id=student_id)

            # Create Student object
            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
            print(f"Created student {student_name} with ID {student_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

def generate_report_card():
    current_rank = -1
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks', 'student_age')
    i = 1
    for rank in ranks:
       ReportCard.objects.create(
           student = rank,
           student_rank = i
       )
       i = i + 1