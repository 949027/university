import xlsxwriter
from university.celery import app
from django.conf import settings

from class_organizer.models import Course, Group


@app.task
def create_report():
    with xlsxwriter.Workbook('report.xlsx') as workbook:
        cell_format = workbook.add_format({'border': 1})

        # лист с направлениями
        worksheet = workbook.add_worksheet('Направления')
        row, col = 0, 0
        for course in Course.objects.select_related('curator__user').prefetch_related('subjects'):
            worksheet.write(row, col, 'Направление', cell_format)
            worksheet.write(row, col + 1, course.name, cell_format)
            row += 1

            worksheet.write(row, col, 'Куратор', cell_format)
            worksheet.write(row, col + 1, course.curator.user.username, cell_format)
            row += 1

            worksheet.write(row, col, 'Дисциплины', cell_format)
            for subject in course.subjects.all():
                worksheet.write(row, col + 1, subject.name, cell_format)
                row += 1
            row += 1

        # лист с группами
        worksheet = workbook.add_worksheet('Группы')
        row = 0
        for group in Group.objects.prefetch_related('students'):
            worksheet.write(row, col, 'Группа', cell_format)
            worksheet.write(row, col + 1, group.name, cell_format)
            row += 1

            worksheet.write(row, col, 'Состав', cell_format)
            for student in group.students.order_by('name'):
                worksheet.write(row, col + 1, student.name, cell_format)
                row += 1

            worksheet.write(row, col, 'Мужчин', cell_format)
            man_amount = group.students.filter(gender='male').count()
            worksheet.write(row, col + 1, man_amount)
            row += 1

            worksheet.write(row, col, 'Женщин', cell_format)
            woman_amount = group.students.filter(gender='female').count()
            worksheet.write(row, col + 1, woman_amount, cell_format)
            row += 1

            worksheet.write(row, col, 'Свободных мест', cell_format)
            vacancies_count = int(settings.MAX_GROUP_SIZE) - group.students.count()
            worksheet.write(row, col + 1, vacancies_count, cell_format)
            row += 2
