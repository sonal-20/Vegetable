

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth  import get_user_model

User = get_user_model()

# Create your models here.

class ReceipesManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted = False)


class StudentManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted = False)
        

class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")
    is_deleted = models.BooleanField(default=False)

    objects = ReceipesManager()
    admin_objects = models.Manager()

    
    def __str__(self):
        return self.receipe_name


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department

    class Meta:
        ordering = ['department']  


class StudentId(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id


class Student(models.Model):
    department = models.ForeignKey(Department, related_name="depart", on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentId, related_name="studentid", on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()
    is_deleted = models.BooleanField(default=False)

    objects = StudentManager()
    admin_objects = models.Manager()
    
    def __str__(self) -> str:
        return self.student_name

    class Meta:
        ordering = ['student_name'] 
        verbose_name = "student"    


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject_name


class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, related_name="studentmarks", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.student.student_name} {self.subject.subject_name}'

    class Meta:
        unique_together = ['student', 'subject']




class ReportCard(models.Model):
    student = models.ForeignKey(Student, related_name="studentreportcard", on_delete=models.CASCADE)
    student_rank = models.IntegerField()
    date_of_report_card_generation = models.DateField(auto_now_add=True)  # Fixed: auto_add sets the creation date automatically

    def __str__(self) -> str:
        return f'ReportCard for {self.student.student_name} (Rank: {self.student_rank})'
