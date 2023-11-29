from django.test import TestCase
from data.models import College, Department, Degree, Course, DegreeCourse


class TestCollegeModel(TestCase):
    def test_create_college(self):
        college = College.objects.create(college_name='Test', college_website='www.test.com', college_description='College Test')
        self.assertIsInstance(college, College)

class TestDepartmentModel(TestCase):
    def setUp(self):
        self.college = College.objects.create(college_name='Test', college_website='www.test.com', college_description='College Test')
    def test_create_department(self):
        department = Department.objects.create(department_name='Test', department_website='www.test.com', department_description='College Test', college_id=self.college.pk)
        self.assertIsInstance(department, Department)

class TestDegreeModel(TestCase):
    def setUp(self):
        self.college = College.objects.create(college_name='Test', college_website='www.test.com', college_description='College Test')
        self.department = Department.objects.create(department_name='Test', department_website='www.test.com', department_description='College Test', college_id=self.college.pk)
    def test_create_department(self):
        degree = Degree.objects.create(degree_name='Test', degree_website='www.test.com', degree_description='College Test', online_degree=False, total_hours = 88, department_id=self.department.pk)
        self.assertIsInstance(degree, Degree)

class TestCourseModel(TestCase):
    def test_create_course(self):
        course = Course.objects.create(course_number='CIDM 111', course_name='Test', course_description='College Test', total_hours = 3)
        self.assertIsInstance(course, Course)

class TestDegreeCourseModel(TestCase):
    def setUp(self):
        self.college = College.objects.create(college_name='Test', college_website='www.test.com', college_description='College Test')
        self.department = Department.objects.create(department_name='Test', department_website='www.test.com', department_description='College Test', college_id=self.college.pk)
        self.degree = Degree.objects.create(degree_name='Test', degree_website='www.test.com', degree_description='College Test', online_degree=False, total_hours = 88, department_id=self.department.pk)
        self.course = Course.objects.create(course_number='CIDM 111', course_name='Test', course_description='College Test', total_hours = 3)
    def test_create_department(self):
        degreecourse = DegreeCourse.objects.create(fiscal_year=2024, is_optional=False,is_core=True,is_degree=False,is_major=False, course_id=self.course.pk, degree_id=self.degree.pk)
        self.assertIsInstance(degreecourse, DegreeCourse)