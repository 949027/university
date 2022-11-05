from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import StudentViewSet, GroupViewSet, CourseViewSet, SubjectViewSet, CreateReportView, ReportView, \
    ReportStatusView

urlpatterns = [
    path('token/', obtain_auth_token, name='obtain_auth_token'),
    path('create-report/', CreateReportView.as_view(), name='create_report'),
    path('status-report/<str:task_id>/', ReportStatusView.as_view(), name='status_report'),
    path('get-report/', ReportView.as_view(), name='get_report'),
]

router = DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')
router.register(r'group', GroupViewSet, basename='group')
router.register(r'course', CourseViewSet, basename='course')
router.register(r'subject', SubjectViewSet, basename='subject')

urlpatterns += router.urls

