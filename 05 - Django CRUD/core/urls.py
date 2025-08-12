# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Departments
    path('departments/', views.department_list_create, name='department-list'),
    path('departments/<int:pk>/', views.department_detail, name='department-detail'),
    path('departments/<int:pk>/full/', views.department_full_view, name='department-full'),

    # Courses
    path('courses/', views.course_list_create, name='course-list'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),

    # Students
    path('students/', views.student_list_create, name='student-list'),
    path('students/<int:pk>/', views.student_detail, name='student-detail'),
]
