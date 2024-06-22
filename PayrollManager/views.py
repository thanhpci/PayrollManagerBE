from django.shortcuts import render

# Create your views here.
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage


from .models import Employee, Department, AttendanceRecord, EmployeeDepartment, Salary, Holiday, Configuration
from .serializers import EmployeeSerializer, AttendanceRecordSerializer, SalarySerializer, DepartmentSerializer, EmployeeDepartmentSerializer, HolidaySerializer, ConfigurationSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name', 'employee_code', 'departments__name']
    ordering_fields = ['name', 'employee_code', 'date_of_birth']
    search_fields = ['name', 'employee_code', 'phone_number', 'date_of_birth']
    # search_fields = ['employee_code']
    ordering = ['name']  # Sắp xếp mặc định


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeDepartmentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDepartment.objects.all()
    serializer_class = EmployeeDepartmentSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer





class UploadAttendanceFileView(APIView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        month = request.data.get('month')
        year = request.data.get('year')

        if not files or not month or not year:
            return Response({'error': 'Files, month, and year are required'}, status=status.HTTP_400_BAD_REQUEST)

        for file in files:
            # Save file temporarily
            file_path = default_storage.save(f'temp/{file.name}', file)

            # Process file
            employee_info, attendance_data = self.process_attendance_file(file_path, month, year)

            # Clean up temporary file
            default_storage.delete(file_path)

            if employee_info is None or attendance_data is None:
                return Response({'error': f'Failed to process the attendance file {file.name}'}, status=status.HTTP_400_BAD_REQUEST)

            # Process employee and attendance data
            employee = self.get_or_create_employee(employee_info)
            if employee is None:
                return Response({'error': f'Failed to process employee data for file {file.name}'}, status=status.HTTP_400_BAD_REQUEST)

            # Add attendance records
            self.add_attendance_records(employee, attendance_data)

        return Response({'message': 'All files processed successfully'}, status=status.HTTP_200_OK)

    def process_attendance_file(self, file_path, month, year):
        try:
            # Parse XML
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Namespace dictionary for XML parsing
            namespaces = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

            # Extract rows and determine the maximum number of columns simultaneously
            rows = []
            max_cols = 0
            for row in root.findall(".//ss:Row", namespaces):
                cells = [cell.text for cell in row.findall("ss:Cell/ss:Data", namespaces)]
                rows.append(cells)
                max_cols = max(max_cols, len(cells))

            # Ensure all rows have the same number of columns
            for row in rows:
                row.extend([None] * (max_cols - len(row)))

            # Extract value of cell A2
            cell_A2 = rows[1][0] if len(rows) > 1 else 'No data'
            employee_info = self.parse_employee_info(cell_A2)

            # Convert to DataFrame
            df = pd.DataFrame(rows[1:], columns=rows[0])  # Assumes first row as header

            # Process DataFrame to extract attendance data for the given month and year
            attendance_data = self.extract_attendance_data(df, month, year)

            return employee_info, attendance_data

        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        return None, None

    def parse_employee_info(self, cell_data):
        try:
            employee_code = self.extract_info(cell_data, "Mã nhân viên:", "Tên nhân viên:")
            employee_name = self.extract_info(cell_data, "Tên nhân viên:", "Bộ phận:")
            department_name = self.extract_info(cell_data, "Bộ phận:", None)
            return {
                'employee_code': employee_code,
                'employee_name': employee_name,
                'department_name': department_name
            }
        except Exception as e:
            print(f"Error parsing employee info: {e}")
            return None

    def extract_info(self, text, start_keyword, end_keyword):
        try:
            start = text.index(start_keyword) + len(start_keyword)
            if end_keyword:
                end = text.index(end_keyword, start)
                return text[start:end].strip()
            else:
                return text[start:].strip()
        except ValueError as e:
            print(f"Error extracting info between '{start_keyword}' and '{end_keyword}': {e}")
            return None

    def extract_attendance_data(self, df, month, year):
        # Convert first column to datetime
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y-%m-%dT%H:%M:%S.%f', errors='coerce')

        # Create start and end dates for the given month and year
        start_date = datetime(int(year), int(month), 1)
        end_date = (start_date + pd.DateOffset(months=1)) - pd.DateOffset(days=1)

        # Filter rows by the given month and year
        filtered_df = df[(df.iloc[:, 0] >= start_date) & (df.iloc[:, 0] <= end_date)]

        # Select relevant columns
        result_df = filtered_df.iloc[:, [0, 2, 3, 4, 5]]

        # Rename columns
        result_df.columns = ['Date', 'Morning In', 'Morning Out', 'Afternoon In', 'Afternoon Out']

        # Convert DataFrame to dictionary
        attendance_data = result_df.to_dict(orient='records')
        return attendance_data

    def get_or_create_employee(self, employee_info):
        try:
            employee_code = employee_info['employee_code']
            employee_name = employee_info['employee_name']
            department_name = " ".join(employee_info['department_name'].split())

            # Kiểm tra xem nhân viên đã tồn tại chưa
            employee = Employee.objects.filter(employee_code=employee_code).first()
            if employee:
                return employee

            # Nếu nhân viên chưa tồn tại, tạo nhân viên mới
            employee = Employee.objects.create(employee_code=employee_code, name=employee_name)

            # Kiểm tra và tạo phòng ban nếu có thông tin
            if department_name:
                # Kiểm tra xem phòng ban đã tồn tại chưa (không phân biệt chữ hoa chữ thường)
                department = Department.objects.filter(name__iexact=department_name).first()
                if not department:
                    # Nếu phòng ban chưa tồn tại, tạo phòng ban mới
                    department = Department.objects.create(name=department_name)

                # Thêm nhân viên vào phòng ban nếu chưa tồn tại
                if not EmployeeDepartment.objects.filter(employee=employee, department=department).exists():
                    EmployeeDepartment.objects.create(employee=employee, department=department)

            return employee
        except Exception as e:
            print(f"Error getting or creating employee: {e}")
            return None

    def add_attendance_records(self, employee, attendance_data):
        try:
            for record in attendance_data:
                # Kiểm tra xem AttendanceRecord đã tồn tại chưa
                if not AttendanceRecord.objects.filter(
                    employee=employee,
                    date=record['Date']
                ).exists():
                    AttendanceRecord.objects.create(
                        employee=employee,
                        date=record['Date'],
                        morning_clock_in=record['Morning In'],
                        morning_clock_out=record['Morning Out'],
                        afternoon_clock_in=record['Afternoon In'],
                        afternoon_clock_out=record['Afternoon Out']
                    )
        except Exception as e:
            print(f"Error adding attendance records: {e}")


class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)



