# core/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Department, Course, Student
from .serializers import (
    DepartmentSerializer, CourseSerializer, StudentSerializer,
    DepartmentNestedSerializer
)

# ---------------------------
# Departments
# ---------------------------

@api_view(['GET', 'POST'])
def department_list_create(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def department_detail(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = DepartmentSerializer(department, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# Courses
# ---------------------------

@api_view(['GET', 'POST'])
def course_list_create(request):
    if request.method == 'GET':
        dept_id = request.query_params.get('department')
        if dept_id:
            courses = Course.objects.filter(department_id=dept_id).select_related('department')
        else:
            courses = Course.objects.select_related('department').all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def course_detail(request, pk):
    try:
        course = Course.objects.select_related('department').get(pk=pk)
    except Course.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = CourseSerializer(course, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# Students
# ---------------------------

@api_view(['GET', 'POST'])
def student_list_create(request):
    if request.method == 'GET':
        course_id = request.query_params.get('course')
        dept_id = request.query_params.get('department')
        students = Student.objects.select_related('course__department').all()

        if course_id:
            students = students.filter(course_id=course_id)
        elif dept_id:
            students = students.filter(course__department_id=dept_id)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.select_related('course__department').get(pk=pk)
    except Student.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = StudentSerializer(student, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# Nested Department -> Courses -> Students
# ---------------------------

@api_view(['GET'])
def department_full_view(request, pk):
    """
    Return Department with nested courses and students
    """
    try:
        dept = Department.objects.prefetch_related('courses__students').get(pk=pk)
    except Department.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DepartmentNestedSerializer(dept)
    return Response(serializer.data)
