from django.conf.urls import url
from django.urls import path, include
from .views import CountCompletedAssignments, GetCourseAverageGrade, CountAssignmentsCreated, SchoolAssignmentCompletionPercentage

app_name = 'api'
urlpatterns = [
    url(r'^CountCompletedAssignments/$', CountCompletedAssignments.as_view()),
    url(r'^GetCourseAverageGrade/$', GetCourseAverageGrade.as_view()),
    url(r'^CountAssignmentsCreated/$', CountAssignmentsCreated.as_view()),
    url(r'^SchoolAssignmentCompletionPercentage/$', SchoolAssignmentCompletionPercentage.as_view()),
]
