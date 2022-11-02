import io

import xlsxwriter
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

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


def create_report():
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)

    worksheet = workbook.add_worksheet('Направления')
    row, col = 0, 0
    for course in Course.objects.all():
        worksheet.write(row, col, 'Направление')
        worksheet.write(row, col + 1, course.name)
        row += 1

        worksheet.write(row, col, 'Куратор')
        worksheet.write(row, col + 1, course.curator.user.first_name)
        row += 1

        worksheet.write(row, col, 'Дисциплины')
        for object in course.subjects.all():
            worksheet.write(row, col + 1, object.name)
            row += 1

    worksheet = workbook.add_worksheet('Группы')
    row = 0
    for group in Group.objects.all():
        worksheet.write(row, col, 'Наименование группы')
        worksheet.write(row, col + 1, group.name)
        row += 1

        worksheet.write(row, col, 'Состав')
        for student in group.students.order_by('name'):
            worksheet.write(row, col + 1, student.name)
            row += 1

        worksheet.write(row, col, 'Мужчин')
        man_amount = group.students.filter(gender='male').count()
        worksheet.write(row, col + 1, man_amount)
        row += 1

        worksheet.write(row, col, 'Женщин')
        woman_amount = group.students.filter(gender='female').count()
        worksheet.write(row, col + 1, woman_amount)

        worksheet.write(row, col, 'Свободных мест')
        vacancies_count = int(settings.MAX_GROUP_SIZE) - group.students.count()
        worksheet.write(row, col + 1, vacancies_count)

    workbook.close()
    buffer.seek(0)
    return buffer


class ReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return FileResponse(create_report(), as_attachment=True, filename='report.xlsx')
