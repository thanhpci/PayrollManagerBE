from django.contrib import admin
from .models import Employee, AttendanceRecord, Salary, Department, EmployeeDepartment, Holiday, Configuration


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'name', 'phone_number', 'date_of_birth', 'created_at', 'updated_at']
    search_fields = ['employee_code', 'name', 'phone_number', 'date_of_birth']
    filter_horizontal = ('departments',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(EmployeeDepartment)
class EmployeeDepartmentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'department', 'created_at', 'updated_at']
    search_fields = ['employee__name', 'department__name']
    list_filter = ['employee', 'department']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'morning_clock_in', 'morning_clock_out', 'afternoon_clock_in',
                    'afternoon_clock_out', 'created_at', 'updated_at']
    search_fields = ['employee__name']
    list_filter = ['employee', 'date']


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'year', 'total_hours', 'salary_amount']
    search_fields = ['employee__name', 'month', 'year']
    list_filter = ['employee', 'month', 'year']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'day', 'month']
    search_fields = ['name']
    list_filter = ['month', 'day']


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['basic_days', 'basic_hours_per_day', 'hourly_wage', 'overtime_multiplier',
                    'worked_day_off_multiplier', 'sunday_multiplier', 'holiday_multiplier']
