from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
