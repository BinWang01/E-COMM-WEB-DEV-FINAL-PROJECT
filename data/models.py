from django.db import models


class College(models.Model):
    college_name = models.CharField(
        max_length=100, help_text="The name of the College."
    )
    college_website = models.URLField(
        blank=True, null=True, help_text="The website of the College."
    )
    college_description = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="The description of the College.",
    )

    def __str__(self) -> str:
        return self.college_name


class Department(models.Model):
    department_name = models.CharField(
        max_length=100, help_text="The name of the Department."
    )
    department_description = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="The description of the Department.",
    )
    department_website = models.URLField(
        blank=True, null=True, help_text="The website of the Department."
    )
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.department_name


class Degree(models.Model):
    degree_name = models.CharField(max_length=100, help_text="The name of the Degree.")
    degree_description = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="The description of the Degree.",
    )
    degree_website = models.URLField(
        blank=True, null=True, help_text="The website of the Degree."
    )
    online_degree = models.BooleanField(default=False)
    total_hours = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.degree_name


class Course(models.Model):
    course_number = models.CharField(
        max_length=100, help_text="The number of the Course."
    )
    course_name = models.CharField(max_length=100, help_text="The name of the Course.")
    course_description = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="The description of the Course.",
    )
    total_hours = models.IntegerField()

    def __str__(self) -> str:
        return self.course_number + ":" + self.course_name


class DegreeCourse(models.Model):
    fiscal_year = models.IntegerField()
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_optional = models.BooleanField(default=False)
    is_core = models.BooleanField()
    is_degree = models.BooleanField()
    is_major = models.BooleanField()

    def __str__(self) -> str:
        return (
            self.degree.degree_name
            + ":"
            + self.course.course_number
            + " "
            + self.course.course_name
        )
