# # from django.contrib import admin
# # from django.db.models import  Sum
# # # Register your models here.
# # from  .models import *

# # admin.site.register(Receipe)
# # admin.site.register(StudentId)
# # admin.site.register(Student)
# # admin.site.register(Department)
# # admin.site.register(Subject)
# # # admin.site.register(SubjectMarks)

# # class SubjectMarkAdmin(admin.ModelAdmin):
# #     list_display = ['student','student_rank','student_marks','date_of_report_card_generation']
# # admin.site.register(SubjectMarks, SubjectMarkAdmin)

# # class ReportCardAdmin(admin.ModelAdmin):
# #     list_display = ['student','subject','marks']
# #     def total_marks(self,obj):
# #         subject_marks = SubjectMarks.objects.filter(student = obj.student)
# #         return obj.aggregate(marks = Sum('marks'))
# # admin.site.register(ReportCard, ReportCardAdmin)

# from django.contrib import admin
# from django.db.models import Sum
# from .models import *

# # Register your models
# admin.site.register(Receipe)
# admin.site.register(StudentId)
# admin.site.register(Student)
# admin.site.register(Department)
# admin.site.register(Subject)

# # Custom admin class for SubjectMarks
# class SubjectMarkAdmin(admin.ModelAdmin):
#     list_display = ['student', 'student_rank', 'student_marks', 'date_of_report_card_generation']

# admin.site.register(SubjectMarks, SubjectMarkAdmin)

# # Custom admin class for ReportCard
# class ReportCardAdmin(admin.ModelAdmin):
#     list_display = ['student', 'subject', 'marks', 'total_marks']  # Add 'total_marks' to display

#     # Method to calculate total marks for a student
#     def total_marks(self, obj):
#         # Get all subject marks for the student in the report card
#         subject_marks = SubjectMarks.objects.filter(student=obj.student)
#         # Aggregate the total marks
#         total = subject_marks.aggregate(total=Sum('marks'))['total']
#         return total

#     total_marks.short_description = 'Total Marks'

# admin.site.register(ReportCard, ReportCardAdmin)


# Import the admin module from django.contrib
from django.contrib import admin
from django.db.models import  Sum
from .models import Receipe, StudentId, Student, Department, Subject, SubjectMarks, ReportCard  # Make sure all models are imported

# Register your models
admin.site.register(Receipe)
admin.site.register(StudentId)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Subject)

# Fix for SubjectMarkAdmin: Display calculated rank and report card date
class SubjectMarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_student_rank', 'marks', 'get_date_of_report_card_generation']

    def get_student_rank(self, obj):
        return obj.student.studentreportcard.student_rank

    def get_date_of_report_card_generation(self, obj):
        return obj.student.studentreportcard.date_of_report_card_generation

    get_student_rank.short_description = 'Student Rank'
    get_date_of_report_card_generation.short_description = 'Report Card Date'

admin.site.register(SubjectMarks, SubjectMarkAdmin)

# Fix for ReportCardAdmin: Display total marks using method
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_total_marks']

    def get_total_marks(self, obj):
        subject_marks = SubjectMarks.objects.filter(student = obj.student)
        marks = (subject_marks.aggregate(marks = Sum('marks')))
        return marks['marks'] 
    get_total_marks.short_description = 'Total Marks'
    
admin.site.register(ReportCard, ReportCardAdmin)
