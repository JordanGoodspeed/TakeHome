from rest_framework import serializers
from api.models import StudentSubmission, Student, Course, CourseWork, Teacher

class StudentSubmissionResource(serializers.ModelSerializer):
    class Meta:
        model = StudentSubmission
        fields = ['submission_id','course_work_id','course_id','student_id','status','assigned_points','max_points']

class StudentResource(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id','school','grade_level','name']

class CourseResource(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id','teacher_id','name']

class CourseWorkResource(serializers.ModelSerializer):
    class Meta:
        model = CourseWork
        fields = ['course_work_id','course_id','title','due_date']
        
class TeacherResource(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_id','name','school']
