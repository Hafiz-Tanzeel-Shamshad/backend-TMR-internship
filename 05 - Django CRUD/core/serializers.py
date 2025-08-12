# core/serializers.py
from rest_framework import serializers
from .models import Department, Course, Student

# Simple nested serializers for read use
class StudentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']


class CourseNestedSerializer(serializers.ModelSerializer):
    # show nested students
    students = StudentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'students']


class DepartmentNestedSerializer(serializers.ModelSerializer):
    # show nested courses -> students
    courses = CourseNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'courses']


# CRUD serializers (support write/read)
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    # write using PK, read you can also see nested department_detail
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    department_detail = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'department', 'department_detail']


class StudentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    # include nested course (which itself includes department_detail)
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'course', 'course_detail']

