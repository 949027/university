from django.contrib import admin
from class_organizer.models import Curator, Student, Course, Group, Subject


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Curator)
class CuratorAdmin(admin.ModelAdmin):
    pass


class GroupInline(admin.TabularInline):
    model = Group
    #readonly_fields = ('gender', )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [GroupInline]


class StudentInline(admin.TabularInline):
    model = Student
    #readonly_fields = ('gender', )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass
