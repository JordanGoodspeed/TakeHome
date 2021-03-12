from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import StudentSubmission, Student, Course, CourseWork, Teacher
import json
from api.serializers import StudentSubmissionResource, StudentResource, CourseResource, CourseWorkResource, TeacherResource
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Avg
from collections import Counter


# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentResource

    @action(methods=['get'], detail=False)
    def assignment_completion_percentage(self, request):
        students = self.get_queryset()
        total_students = students.values('school').annotate(numStudents=Count('school'))
        total_students = {i['school']: i['numStudents'] for i in total_students}
        studentOverThreshold = StudentSubmission.objects.filter(status=2).values('student_id').annotate(numCompleted=Count('status')).filter(numCompleted__gt=1).values('student_id')
        studentOverThresholdSchools = students.filter(student_id__in=studentOverThreshold).values('school').annotate(numStudents=Count('school'))
        percent_dict = {i['school']: (i['numStudents'] / total_students[i['school']]) * 100 for i in studentOverThresholdSchools}
        completion_percentages = [{'school':key, 'numStudents':value} for key,value in percent_dict.items()]
        serializer = json.dumps(list(completion_percentages), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)

class StudentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = StudentSubmission.objects.all()
    serializer_class = StudentSubmissionResource

    @action(methods=['get'], detail=False)
    def count_completed(self, request):
        completed_assignments = self.get_queryset().filter(status=2).values('student_id').annotate(assignmentsComplete=Count('status'))
        serializer = json.dumps(list(completed_assignments), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def course_average(self, request):
        average_grade = self.get_queryset().filter(status=2).values('course_id').annotate(avgGrade=Avg('assigned_points'))
        serializer = json.dumps(list(average_grade), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherResource

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseResource

class CourseWorkViewSet(viewsets.ModelViewSet):
    queryset = CourseWork.objects.all()
    serializer_class = CourseWorkResource

    @action(methods=['get'], detail=False)
    def count_assignments(self, request):
        assignments_created = self.get_queryset()
        assignments_created = Counter([i.course_id.teacher_id.teacher_id for i in assignments_created])
        assignments_created = [{'teacher_id':key, 'assignmentsCreated':value} for key,value in assignments_created.items()]
        serializer = json.dumps(list(assignments_created), cls=DjangoJSONEncoder)
        return Response(serializer, status=status.HTTP_200_OK)
