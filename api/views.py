from celery.result import AsyncResult
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from class_organizer.tasks import create_report
from .serializers import StudentSerializer, GroupSerializer, CourseSerializer, SubjectSerializer
from class_organizer.models import Student, Group, Course, Subject


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class CreateReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        task = create_report.delay()
        return Response({'task_id': task.id})


class ReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            report = open('report.xlsx', 'rb')
            return FileResponse(report, as_attachment=False, filename='report.xlsx')
        except FileNotFoundError:
            return Response({'error': 'report not created'})


class ReportStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
        }
        return Response(result)
