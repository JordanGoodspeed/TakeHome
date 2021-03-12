from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .views import StudentViewSet, StudentSubmissionViewSet, TeacherViewSet, CourseViewSet, CourseWorkViewSet

router = routers.SimpleRouter()

router.register(r'students', StudentViewSet)
router.register(r'student_submissions', StudentSubmissionViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'coursework', CourseWorkViewSet)

app_name = 'api'

urlpatterns = [
    url(r'^', include(router.urls)),
]
