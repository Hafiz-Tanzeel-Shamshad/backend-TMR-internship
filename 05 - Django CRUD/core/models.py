# core/models.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CourseQuerySet(models.QuerySet):
    def for_department(self, dept_id):
        """Custom queryset method to filter courses by department id"""
        return self.filter(department_id=dept_id)


class Course(models.Model):
    name = models.CharField(max_length=255)
    # related_name makes nested serializers easier (department.courses)
    department = models.ForeignKey(Department, related_name='courses', on_delete=models.CASCADE)

    # Attach our custom queryset as manager
    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} ({self.department})"


class Student(models.Model):
    name = models.CharField(max_length=255)
    # related_name lets us access course.students
    course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.course.name}"
