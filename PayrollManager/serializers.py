from rest_framework import serializers
from .models import Employee, AttendanceRecord, Salary, Department, EmployeeDepartment, Holiday, Configuration


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDepartment
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = Salary
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
