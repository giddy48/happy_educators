from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_home, name="dashboard"),
    path('students/', views.students_view, name='students'),
    path("student/<int:id>/", views.student_detail, name="student_detail"),
    path("enter-marks/", views.enter_marks, name="enter_marks"),
    path('classes/', views.class_list, name='class_list'),
    path("teacher-dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path('enter-marks/', views.enter_marks, name='enter_marks'),
    path('results/', views.results, name='results'),
    path('report-card/', views.results, name='report_card'),
    path('report-card/bulk/<int:class_id>/', views.bulk_report_card_pdf, name='bulk_report_card_pdf'),
    path('report-card/<int:class_id>/<int:student_id>/', views.report_card_pdf, name='report_card_pdf'),
    path('bulk-report/<int:class_id>/', views.bulk_report_card_pdf, name='bulk_report_card_pdf'),
    path('', views.login_view, name='login')
]


