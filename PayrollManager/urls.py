from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EmployeeViewSet, AttendanceRecordViewSet, SalaryViewSet, DepartmentViewSet,
                    EmployeeDepartmentViewSet, UploadAttendanceFileView, DepartmentListView,
                    SalaryCalculationView, EmployeeMonthlyAttendanceView,
                    SalaryAvailableMonthsView, SalaryAvailableYearsView,
                    export_employee_salary_report, export_salary_summary)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employee_departments', EmployeeDepartmentViewSet)
router.register(r'attendance_records', AttendanceRecordViewSet)
router.register(r'salaries', SalaryViewSet)



urlpatterns = [
    path('calculate-salary/', SalaryCalculationView.as_view(), name='calculate-salary'),
    path('upload-attendance-file/', UploadAttendanceFileView.as_view(), name='upload-attendance-file'),
    path('departments/all/', DepartmentListView.as_view(), name='all-departments'),  # Endpoint không phân trang
    path('employee-monthly-attendance/', EmployeeMonthlyAttendanceView.as_view(), name='employee-monthly-attendance'),
    path('salary/available-months/', SalaryAvailableMonthsView.as_view(), name='salary-available-months'),
    path('salary/available-years/', SalaryAvailableYearsView.as_view(), name='salary-available-years'),
    path('export_employee_salary_report/<str:employee_code>/<int:month>/<int:year>/', export_employee_salary_report, name='export-employee-salary-report'),

    path('export_salary_summary/', export_salary_summary, name='export-salary-summary'),

    path('', include(router.urls)),
]
