from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudentSubmission, Student, Course, CourseWork, Teacher
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Avg
from collections import Counter


# Create your views here.
class CountCompletedAssignments(APIView):
    def get(self, request):
        completed_assignments = StudentSubmission.objects.filter(status=2).values('student_id').annotate(assignmentsComplete=Count('status'))
        serializer = json.dumps(list(completed_assignments), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)
        

class GetCourseAverageGrade(APIView):
    def get(self, request):
        average_grade = StudentSubmission.objects.filter(status=2).values('course_id').annotate(avgGrade=Avg('assigned_points'))
        serializer = json.dumps(list(average_grade), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)

class CountAssignmentsCreated(APIView):
    def get(self, request):
        assignments_created = CourseWork.objects.all()
        assignments_created = Counter([i.course_id.teacher_id.teacher_id for i in assignments_created])
        assignments_created = [{'teacher_id':key, 'assignmentsCreated':value} for key,value in assignments_created.items()]
        serializer = json.dumps(list(assignments_created), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)

class SchoolAssignmentCompletionPercentage(APIView):
    def get(self, request):
        total_students = Student.objects.values('school').annotate(numStudents=Count('school'))
        total_students = {i['school']: i['numStudents'] for i in total_students}
        studentOverThreshold = StudentSubmission.objects.filter(status=2).values('student_id').annotate(numCompleted=Count('status')).filter(numCompleted__gt=1).values('student_id')
        studentOverThresholdSchools = Student.objects.filter(student_id__in=studentOverThreshold).values('school').annotate(numStudents=Count('school'))
        percent_dict = {i['school']: (i['numStudents'] / total_students[i['school']]) * 100 for i in studentOverThresholdSchools}
        completion_percentages = [{'school':key, 'numStudents':value} for key,value in percent_dict.items()]
        serializer = json.dumps(list(completion_percentages), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)
