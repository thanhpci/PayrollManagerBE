from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EmployeeViewSet, AttendanceRecordViewSet, SalaryViewSet, DepartmentViewSet,
                    EmployeeDepartmentViewSet, UploadAttendanceFileView, DepartmentListView,
                    SalaryCalculationView, EmployeeMonthlyAttendanceView)

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
    # Thêm đường dẫn mới

    path('', include(router.urls)),
]
