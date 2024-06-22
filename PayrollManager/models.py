from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Tên phòng ban
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_code = models.CharField(max_length=10, unique=True)  # Mã nhân viên
    name = models.CharField(max_length=100)  # Tên
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại
    date_of_birth = models.DateField(blank=True, null=True)  # Ngày sinh
    departments = models.ManyToManyField(Department,
                                         through='EmployeeDepartment')  # Mối quan hệ nhiều-nhiều với Department

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmployeeDepartment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Nhân viên
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Phòng ban
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'department')

    def __str__(self):
        return f"{self.employee.name} - {self.department.name}"


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Nhân viên
    date = models.DateField()  # Ngày
    morning_clock_in = models.TimeField(null=True, blank=True)  # Giờ vào buổi sáng
    morning_clock_out = models.TimeField(null=True, blank=True)  # Giờ ra buổi sáng
    afternoon_clock_in = models.TimeField(null=True, blank=True)  # Giờ vào buổi chiều
    afternoon_clock_out = models.TimeField(null=True, blank=True)  # Giờ ra buổi chiều
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')  # Đảm bảo không có bản ghi chấm công trùng lặp

    def __str__(self):
        return f"{self.employee.name} - {self.date}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Nhân viên
    month = models.IntegerField()  # Tháng tính lương (1-12)
    year = models.IntegerField()  # Năm tính lương
    # basic_days = models.IntegerField()  # Số ngày cơ bản
    basic_days_after_holidays = models.IntegerField()  # Số ngày cơ bản sau lễ
    # basic_hours = models.FloatField()  # Số giờ cơ bản
    basic_hours_after_holidays = models.FloatField()  # Số giờ cơ bản sau lễ
    actual_work_hours = models.FloatField()  # Số giờ làm việc thực tế
    worked_days = models.IntegerField()  # Số ngày đi làm
    penalty_hours = models.FloatField()  # Số giờ vi phạm
    worked_day_off_days = models.IntegerField()  # Số ngày nghỉ đi làm
    sunday_hours = models.FloatField()  # Số giờ làm vào Chủ nhật
    holiday_hours = models.FloatField()  # Số giờ lễ
    worked_holiday_hours = models.FloatField()  # Số giờ làm ngày lễ
    average_hours_per_day = models.FloatField()  # Số giờ làm trung bình mỗi ngày
    worked_day_off_hours = models.FloatField()  # Số giờ nghỉ đi làm
    overtime_hours = models.FloatField()  # Số giờ làm thêm
    total_hours = models.FloatField()  # Tổng số giờ
    salary_amount = models.FloatField()  # Tổng số tiền lương
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')  # Đảm bảo không có bản ghi lương trùng lặp

    def __str__(self):
        return f"{self.employee.name} - {self.month}"


class Holiday(models.Model):
    name = models.CharField(max_length=100)  # Tên ngày lễ
    month = models.IntegerField()  # Tháng của ngày lễ (1-12)
    day = models.IntegerField()  # Ngày của ngày lễ (1-31)

    def __str__(self):
        return f"{self.name} ({self.day}/{self.month})"

    class Meta:
        unique_together = ('month', 'day')  # Đảm bảo không có ngày lễ trùng lặp
        ordering = ['month', 'day']  # Sắp xếp theo ngày tháng


class Configuration(models.Model):
    basic_days = models.IntegerField()  # Số ngày cơ bản của tháng
    basic_hours_per_day = models.FloatField()  # Số giờ cơ bản của ngày
    hourly_wage = models.FloatField()  # Giá tiền giờ cơ bản

    overtime_multiplier = models.FloatField(default=1.5)  # Hệ số nhân cho giờ làm thêm
    worked_day_off_multiplier = models.FloatField(default=2.0)  # Hệ số nhân cho giờ nghỉ đi làm
    sunday_multiplier = models.FloatField(default=2.0)  # Hệ số nhân cho giờ làm Chủ nhật
    holiday_multiplier = models.FloatField(default=3.0)  # Hệ số nhân cho giờ làm ngày lễ

    def __str__(self):
        return "Configuration"

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"
