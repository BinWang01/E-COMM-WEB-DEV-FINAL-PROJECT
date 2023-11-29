from django.http import FileResponse, HttpResponse
from requests import request
from data.models import College, Department, Degree, Course, DegreeCourse
from django.shortcuts import render, get_object_or_404, redirect
from data.forms import (
    CollegeForm,
    DepartmentForm,
    DegreeForm,
    CourseForm,
    DegreeCourseForm,
    UploadFileForm
)
from django.contrib import messages
import pandas as pd
from io import StringIO, BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test, login_required
import csv
from PIL import Image
import os
from django.conf import settings
from django.db.models import Count
from plotly.offline import plot
import plotly.graph_objects as graphs

class AboutView(TemplateView):
    template_name = "about.html"


def is_admin(user):
    return user.groups.filter(name="admingroup").exists() or user.is_superuser

def index(request):
    degreecourses = (
        DegreeCourse.objects.select_related("degree").select_related("course").all()
    )
    return render(request, "index.html", {"items": degreecourses})


def view(request):
    degreecourses = (
        DegreeCourse.objects.select_related("degree").select_related("course").all()
    )
    return render(request, "view.html", {"items": degreecourses})

@login_required
@user_passes_test(is_admin)
def manage(request):
    data = DegreeCourse.objects.values("degree_id").annotate(course_count=Count('course_id')).order_by('degree_id')
    df = pd.DataFrame(data)
    df["degree_name"]=""
    for index, row in df.iterrows():
        df.at[index, 'degree_name'] = Degree.objects.filter(id=row['degree_id']).get().degree_name
    figure = graphs.Figure()
    scatter = graphs.Bar(x=df["degree_name"], y=df["course_count"])
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Degree", yaxis_title="No. of Courses")
    plot_html = plot(figure, output_type='div')
    return render(request, "manage.html",{'raw_data':df,'data':plot_html})

@login_required
@user_passes_test(is_admin)
def bulk_upload(request):
    return render(request, "bulk_upload.html")

@login_required
@user_passes_test(is_admin)
def college_list(request):
    colleges = College.objects.all()
    return render(request, "college/college-list.html", {"colleges": colleges})

@login_required
@user_passes_test(is_admin)
def college_edit(request, pk=None):
    if pk is not None:
        college = get_object_or_404(College, pk=pk)
    else:
        college = None

    if request.method == "POST":
        form = CollegeForm(request.POST, instance=college)
        if form.is_valid():
            updated_college = form.save()
            if college is None:
                messages.success(
                    request, 'College "{}" was created.'.format(updated_college)
                )
            else:
                messages.success(
                    request, 'College "{}" was updated.'.format(updated_college)
                )

            return redirect("college_list")
    else:
        form = CollegeForm(instance=college)

    return render(
        request,
        "instance-form.html",
        {
            "method": request.method,
            "form": form,
            "model_type": "College",
            "instance": college,
        },
    )

@login_required
@user_passes_test(is_admin)
def college_import(request):
    csv = request.FILES["csv_file"]
    csv_data = pd.read_csv(StringIO(csv.read().decode("utf-8")))
    for record in csv_data.to_dict(orient="records"):
        if (
            College.objects.filter(college_name=record["college_name"]).exists()
            == False
        ):
            data_dict = {}
            data_dict["college_name"] = record["college_name"]
            data_dict["college_website"] = record["college_website"]
            data_dict["college_description"] = record["college_description"]
            form = CollegeForm(data_dict)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'College "{}" was created.'.format(record["college_name"])
                )
        else:
            messages.info(
                request,
                'College "{}" already exits. Row skipped.'.format(
                    record["college_name"]
                ),
            )
    return redirect("college_list")

@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.select_related("college").all()
    return render(
        request, "department/department-list.html", {"departments": departments}
    )

@login_required
@user_passes_test(is_admin)
def department_edit(request, pk=None):
    if pk is not None:
        department = get_object_or_404(Department, pk=pk)
    else:
        department = None

    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            updated_department = form.save()
            if department is None:
                messages.success(
                    request, 'Department "{}" was created.'.format(updated_department)
                )
            else:
                messages.success(
                    request, 'Department "{}" was updated.'.format(updated_department)
                )

            return redirect("department_list")
    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        "instance-form.html",
        {
            "method": request.method,
            "form": form,
            "model_type": "Department",
            "instance": department,
        },
    )

@login_required
@user_passes_test(is_admin)
def department_import(request):
    csv = request.FILES["csv_file"]
    csv_data = pd.read_csv(StringIO(csv.read().decode("utf-8")))
    for record in csv_data.to_dict(orient="records"):
        if (
            Department.objects.filter(
                department_name=record["department_name"]
            ).exists()
            == False
        ):
            data_dict = {}
            data_dict["department_name"] = record["department_name"]
            data_dict["department_website"] = record["department_website"]
            data_dict["department_description"] = record["department_description"]
            data_dict["college"] = int(record["college_id"])
            form = DepartmentForm(data_dict)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Department "{}" was created.'.format(record["department_name"]),
                )
        else:
            messages.info(
                request,
                'Department "{}" already exits. Row skipped.'.format(
                    record["department_name"]
                ),
            )
    return redirect("department_list")

@login_required
@user_passes_test(is_admin)
def degree_list(request):
    degrees = Degree.objects.select_related("department").all()
    return render(request, "degree/degree-list.html", {"degrees": degrees})

@login_required
@user_passes_test(is_admin)
def degree_edit(request, pk=None):
    if pk is not None:
        degree = get_object_or_404(Degree, pk=pk)
    else:
        degree = None

    if request.method == "POST":
        form = DegreeForm(request.POST, instance=degree)
        if form.is_valid():
            updated_degree = form.save()
            if degree is None:
                messages.success(
                    request, 'Degree "{}" was created.'.format(updated_degree)
                )
            else:
                messages.success(
                    request, 'Degree "{}" was updated.'.format(updated_degree)
                )

            return redirect("degree_list")
    else:
        form = DegreeForm(instance=degree)

    return render(
        request,
        "instance-form.html",
        {
            "method": request.method,
            "form": form,
            "model_type": "Degree",
            "instance": degree,
        },
    )

@login_required
@user_passes_test(is_admin)
def degree_import(request):
    csv = request.FILES["csv_file"]
    csv_data = pd.read_csv(StringIO(csv.read().decode("utf-8")))
    for record in csv_data.to_dict(orient="records"):
        if Degree.objects.filter(degree_name=record["degree_name"]).exists() == False:
            data_dict = {}
            data_dict["degree_name"] = record["degree_name"]
            data_dict["degree_description"] = record["degree_description"]
            data_dict["degree_website"] = record["degree_website"]
            data_dict["online_degree"] = bool(record["online_degree"])
            data_dict["total_hours"] = int(record["total_hours"])
            data_dict["department"] = int(record["department_id"])
            form = DegreeForm(data_dict)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Degree "{}" was created.'.format(record["degree_name"])
                )
        else:
            messages.info(
                request,
                'Degree "{}" already exits. Row skipped.'.format(record["degree_name"]),
            )
    return redirect("degree_list")

@login_required
@user_passes_test(is_admin)
def course_list(request):
    courses = Course.objects.all()
    return render(request, "course/course-list.html", {"courses": courses})

@login_required
@user_passes_test(is_admin)
def course_edit(request, pk=None):
    if pk is not None:
        course = get_object_or_404(Course, pk=pk)
    else:
        course = None

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            updated_course = form.save()
            if course is None:
                messages.success(
                    request, 'Course "{}" was created.'.format(updated_course)
                )
            else:
                messages.success(
                    request, 'Course "{}" was updated.'.format(updated_course)
                )

            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "instance-form.html",
        {
            "method": request.method,
            "form": form,
            "model_type": "Course",
            "instance": course,
        },
    )

@login_required
@user_passes_test(is_admin)
def course_import(request):
    csv = request.FILES["csv_file"]
    csv_data = pd.read_csv(StringIO(csv.read().decode("utf-8")))
    for record in csv_data.to_dict(orient="records"):
        if (
            Course.objects.filter(course_number=record["course_number"]).exists()
            == False
        ):
            data_dict = {}
            data_dict["course_number"] = record["course_number"]
            data_dict["course_name"] = record["course_name"]
            data_dict["course_description"] = record["course_description"]
            data_dict["total_hours"] = int(record["total_hours"])
            form = CourseForm(data_dict)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Course "{}: {}" was created.'.format(
                        record["course_number"], record["course_name"]
                    ),
                )
        else:
            messages.info(
                request,
                'Course "{}: {}" already exits. Row skipped.'.format(
                    record["course_number"], record["course_name"]
                ),
            )
    return redirect("course_list")

@login_required
@user_passes_test(is_admin)
def degreecourse_list(request):
    degreecourses = (
        DegreeCourse.objects.select_related("degree").select_related("course").all()
    )
    return render(
        request, "degreecourse/degreecourse-list.html", {"degreecourses": degreecourses}
    )

@login_required
@user_passes_test(is_admin)
def degreecourse_edit(request, pk=None):
    if pk is not None:
        degreecourse = get_object_or_404(DegreeCourse, pk=pk)
    else:
        degreecourse = None

    if request.method == "POST":
        form = DegreeCourseForm(request.POST, instance=degreecourse)
        if form.is_valid():
            updated_degreecourse = form.save()
            if degreecourse is None:
                messages.success(
                    request,
                    'Degree Course "{}" was created.'.format(updated_degreecourse),
                )
            else:
                messages.success(
                    request,
                    'Degree Course "{}" was updated.'.format(updated_degreecourse),
                )

            return redirect("degreecourse_list")
    else:
        form = DegreeCourseForm(instance=degreecourse)

    return render(
        request,
        "instance-form.html",
        {
            "method": request.method,
            "form": form,
            "model_type": "DegreeCourse",
            "instance": degreecourse,
        },
    )

@login_required
@user_passes_test(is_admin)
def degreecourse_import(request):
    csv = request.FILES["csv_file"]
    csv_data = pd.read_csv(StringIO(csv.read().decode("utf-8")))
    for record in csv_data.to_dict(orient="records"):
        if (
            DegreeCourse.objects.filter(fiscal_year=int(record["fiscal_year"]))
            .filter(degree_id=int(record["degree_id"]))
            .filter(course_id=int(record["course_id"]))
            .exists()
            == False
        ):
            data_dict = {}
            data_dict["fiscal_year"] = int(record["fiscal_year"])
            data_dict["degree"] = int(record["degree_id"])
            data_dict["course"] = int(record["course_id"])
            data_dict["is_optional"] = bool(record["is_optional"])
            data_dict["is_core"] = bool(record["is_core"])
            data_dict["is_degree"] = bool(record["is_degree"])
            data_dict["is_major"] = bool(record["is_major"])
            form = DegreeCourseForm(data_dict)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Degree Course: "fiscal year {}, degree id {}, course_id {}" was created.'.format(
                        record["fiscal_year"], record["degree_id"], record["course_id"]
                    ),
                )
        else:
            messages.info(
                request,
                'Degree Course "fiscal year {}, degree id {}, course_id {}" already exits. Row skipped.'.format(
                    record["fiscal_year"], record["degree_id"], record["course_id"]
                ),
            )
    return redirect("degreecourse_list")


def generate_pdf(request, fiscal_year, id):
    degreecourses = (
        DegreeCourse.objects.filter(fiscal_year=fiscal_year)
        .filter(degree_id=id)
        .select_related("degree")
        .select_related("course")
        .all()
    )
    coremappings = []
    degreemappings = []
    majormappings = []
    isoptional = ""
    for record in degreecourses:
        if record.is_core:
            if record.is_optional:
                isoptional = ""
            else:
                isoptional = " (Required)"
            coremappings.append(
                record.course.course_number
                + ": "
                + record.course.course_name
                + isoptional
            )
        if record.is_degree:
            if record.is_optional:
                isoptional = ""
            else:
                isoptional = " (Required)"
            degreemappings.append(
                record.course.course_number
                + ": "
                + record.course.course_name
                + isoptional
            )
        if record.is_major:
            if record.is_optional:
                isoptional = ""
            else:
                isoptional = " (Required)"
            majormappings.append(
                record.course.course_number
                + ": "
                + record.course.course_name
                + isoptional
            )
    result = {
        "fiscal_year": str(fiscal_year),
        "degree": Degree.objects.filter(id=id).first().degree_name,
        "coremappings": coremappings,
        "degreemappings": degreemappings,
        "majormappings": majormappings,
    }

    response = FileResponse(
        generate_pdf_file(result), as_attachment=True, filename="degree_checklist.pdf"
    )
    return response


def generate_pdf_file(result):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(
        100,
        750,
        "Degree Checklist - " + result["fiscal_year"] + " " + result["degree"],
    )
    p.drawString(100, 700, "Core:")
    y = 670
    unit = 0
    counter = 0
    for item in result["coremappings"]:
        p.drawString(100, y - unit * 20, item)
        unit = unit + 1
        counter = counter + 1
    y = y - counter * 20 - 30
    unit = 1
    counter = 0
    p.drawString(100, y, "Degree:")
    for item in result["degreemappings"]:
        p.drawString(100, y - unit * 20, item)
        unit = unit + 1
        counter = counter + 1
    y = y - counter * 20 - 30
    unit = 1
    counter = 0
    p.drawString(100, y, "Major:")
    for item in result["majormappings"]:
        p.drawString(100, y - unit * 20, item)
        unit = unit + 1
        counter = counter + 1

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def generate_csv(request, fiscal_year, id):
    data = (
        DegreeCourse.objects.filter(fiscal_year=fiscal_year)
        .filter(degree_id=id)
        .select_related("degree")
        .select_related("course")
        .all()
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="degree_checklist.csv"'
    writer = csv.writer(response)
    required_course = ""
    writer.writerow(['Fiscal Year', "Degree", "Course","Required"])
    for row in data:
        if row.is_optional:
            required_course = "No"
        else:
            required_course = "Yes"
        writer.writerow([row.fiscal_year, row.degree.degree_name,row.course.course_number+":"+row.course.course_name, required_course])
    return response

@login_required
@user_passes_test(is_admin)
def image_upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        handle_uploaded_file(request.FILES["file"])
        return redirect("upload_success")
    else:
        form = UploadFileForm()
        return render(request, "image-upload.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT, "img", "home.jpg"), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
@login_required
@user_passes_test(is_admin)
def upload_success(request):
    return render(request, "upload-success.html")