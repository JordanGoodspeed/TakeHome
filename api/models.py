from django.db import models
from .utils import StatusTypes

# Create your models here.
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    school = models.CharField(max_length=200)
    grade_level = models.IntegerField()
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    teacher_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class CourseWork(models.Model):
    course_work_id = models.IntegerField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    
    def __str__(self):
        return self.title

class StudentSubmission(models.Model):
    submission_id = models.IntegerField(primary_key=True)
    course_work_id = models.ForeignKey(CourseWork, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusTypes.choices(), default=StatusTypes.NEW)
    assigned_points = models.FloatField()
    max_points = models.FloatField()
    
    def get_status_type_label(self):
        return StatusTypes(self.status).name.title()

