from django.urls import path, include
from .views import Students, Teachers, Classroom

urlpatterns = [
    # For Classroom
    path('', Classroom.home, name='home'),
    path('dashboard', Classroom.dashboard, name='dashboard'),
    path('<int:class_id>/view_class', Classroom.view_class, name='view_class'),
    path('<int:class_id>/people', Classroom.people, name='people'),
    path('profile', Classroom.profile, name='profile'),
    path('password', Classroom.password, name='password'),

    path('signup', Classroom.signup, name='signup'),
    path('login', Classroom.login, name='login'),
    path('logout', Classroom.logout, name='logout'),
    
    # For Students 
    path('join_class', Students.join_class, name='join_class'),
    path('<int:test_id>/attend_test', Students.attend_test, name='attend_test'),
    path('<int:test_id>/submit_test', Students.submit_test, name='submit_test'),
    path('<int:test_id>/review_test', Students.review_test, name='review_test'),
    path('<int:class_id>/assigned_test', Students.assigned_test, name='assigned_test'),
    path('<int:class_id>/missing_test', Students.missing_test, name='missing_test'),
    path('<int:class_id>/done_test', Students.done_test, name='done_test'),

    # For Teachers 
    path('create_class', Teachers.create_class, name='create_class'),
    path('<int:class_id>/update_class', Teachers.update_class, name='update_class'),
    path('<int:class_id>/delete_class', Teachers.delete_class, name='delete_class'),
    path('<int:class_id>/create_test', Teachers.create_test, name='create_test'),
    path('<int:test_id>/update_test', Teachers.update_test, name='update_test'),
    path('<int:test_id>/delete_test', Teachers.delete_test, name='delete_test'),
    path('<int:test_id>/view_test', Teachers.view_test, name='view_test'),
    path('<int:test_id>/students_work', Teachers.students_work, name='students_work'),
    path('<int:test_id>/<int:student_id>/individual_work', Teachers.individual_work, name='individual_work'),
    path('<int:qn_id>/<int:student_id>/update_work', Teachers.update_work, name='update_work'),
    path('<int:test_id>/create_qn', Teachers.create_qn, name='create_qn'),
    path('<int:qn_id>/update_qn', Teachers.update_qn, name='update_qn'),
    path('<int:qn_id>/delete_qn', Teachers.delete_qn, name='delete_qn'),
    
    # Add the new routes
    path('<int:class_id>/submit_question_paper', Teachers.submit_question_paper, name='submit_question_paper'),
    path('download_excel_template', Teachers.download_excel_template, name='download_excel_template'),
    
    # Django Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]
