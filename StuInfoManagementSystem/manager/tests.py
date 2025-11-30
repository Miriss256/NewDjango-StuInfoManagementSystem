from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import manager, teacher, student
from datetime import date


def _valid_teacher_data():
    return {
        'uid': 1,
        'name': 'Mr. Smith',
        'age': 45,
        'gender': 1,
        'create_time': date(2023, 1, 1),
        'salary': 5000.00,
        'password': 'teacherpass',
        'department': 2,
        'faculty': 'Science',
        'level': 2,
        'phone_number': '13800138000',
    }


def _valid_student_data():
    return {
        'name': 'John Doe',
        'age': 20,
        'img': 'StudentTx/test.png',
        'gender': 1,
        'password': 'studentpass',
        'grade': 2,
        'classes': '2A',
        'major': 'Computer Science',
        'studentid': 10001,
        'faculty': 'Engineering',
        'address': '123 Main St',
        'phone_number': '13800138001',
    }


class ManagerModelTests(TestCase):
    """Tests for the `manager` model."""

    def test_create_manager(self):
        m = manager.objects.create(name='admin', password='password123')
        self.assertEqual(m.name, 'admin')
        self.assertEqual(m.password, 'password123')


class TeacherModelTests(TestCase):
    """Tests for the `teacher` model, including validation."""

    @classmethod
    def setUpTestData(cls):
        cls.data = _valid_teacher_data()
        cls.instance = teacher.objects.create(**cls.data)

    def test_fields_saved(self):
        self.assertEqual(self.instance.name, self.data['name'])
        self.assertEqual(self.instance.department, self.data['department'])

    def test_gender_choice_validation(self):
        t = teacher(**self.data)
        t.gender = 3  # invalid choice
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_phone_number_validation(self):
        t = teacher(**self.data)
        t.phone_number = '12345678901'  # invalid format
        with self.assertRaises(ValidationError):
            t.full_clean()


class StudentModelTests(TestCase):
    """Tests for the `student` model."""

    @classmethod
    def setUpTestData(cls):
        cls.data = _valid_student_data()
        cls.instance = student.objects.create(**cls.data)

    def test_fields_saved(self):
        self.assertEqual(self.instance.name, self.data['name'])
        self.assertEqual(self.instance.major, self.data['major'])

    def test_phone_number_validation(self):
        s = student(**self.data)
        s.phone_number = '12345678901'  # invalid format
        with self.assertRaises(ValidationError):
            s.full_clean()

