from django.contrib import admin
from data.models import College, Department, Degree, Course, DegreeCourse

class CollegeAdmin(admin.ModelAdmin):
    list_display=["college_name","college_description"]
    list_filter=["college_name"]
    search_fields=["college_name","college_description"]

class DepartmentAdmin(admin.ModelAdmin):
    list_display=["department_name","department_description"]
    list_filter=["department_name"]
    search_fields=["department_name","department_description"]

class DegreeAdmin(admin.ModelAdmin):
    list_display=["degree_name","degree_description"]
    list_filter=["degree_name"]
    search_fields=["degree_name","degree_description"]

class CourseAdmin(admin.ModelAdmin):
    list_display=["course_number","course_name"]
    list_filter=["course_name"]
    search_fields=["course_number","course_name"]

class DegreeCourseAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(College,CollegeAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Degree,DegreeAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(DegreeCourse,DegreeCourseAdmin)
