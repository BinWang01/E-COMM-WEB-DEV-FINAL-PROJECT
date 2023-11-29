from django.urls import path
from . import views
from data.views import AboutView

urlpatterns = [
    path("", views.index),
    path("about/", AboutView.as_view()),
    path("view", views.view, name="view"),
    path("managecontent", views.manage, name="manage"),
    path("colleges/", views.college_list, name="college_list"),
    path("colleges/<int:pk>/", views.college_edit, name="college_edit"),
    path("colleges/new/", views.college_edit, name="college_create"),
    path("colleges/import", views.college_import, name="college_import"),
    path("departments/", views.department_list, name="department_list"),
    path("departments/<int:pk>/", views.department_edit, name="department_edit"),
    path("departments/new/", views.department_edit, name="department_create"),
    path("departments/import", views.department_import, name="department_import"),
    path("degrees/", views.degree_list, name="degree_list"),
    path("degrees/<int:pk>/", views.degree_edit, name="degree_edit"),
    path("degrees/new/", views.degree_edit, name="degree_create"),
    path("degrees/import", views.degree_import, name="degree_import"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:pk>/", views.course_edit, name="course_edit"),
    path("courses/new/", views.course_edit, name="course_create"),
    path("courses/import", views.course_import, name="course_import"),
    path("degreecourses/", views.degreecourse_list, name="degreecourse_list"),
    path("degreecourses/<int:pk>/", views.degreecourse_edit, name="degreecourse_edit"),
    path("degreecourses/new/", views.degreecourse_edit, name="degreecourse_create"),
    path("degreecourses/import", views.degreecourse_import, name="degreecourse_import"),
    path("bulkupload/", views.bulk_upload, name="bulk_upload"),
    path(
        "generate-pdf/<int:fiscal_year>/<int:id>",
        views.generate_pdf,
        name="generate_pdf",
    ),
    path(
        "generate-csv/<int:fiscal_year>/<int:id>",
        views.generate_csv,
        name="generate_csv",
    ),
    path("imageupload", views.image_upload, name="image_upload"),
    path("upload_success/", views.upload_success, name="upload_success"),
]
