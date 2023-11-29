from django import forms
from data.models import College, Department, Degree, Course, DegreeCourse

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = "__all__"

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"

class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = "__all__"

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class DegreeCourseForm(forms.ModelForm):
    class Meta:
        model = DegreeCourse
        fields = "__all__"

class UploadFileForm(forms.Form):
    file = forms.FileField()