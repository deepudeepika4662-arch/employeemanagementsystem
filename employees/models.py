from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_employee_id():
    return 'EMP' + uuid.uuid4().hex[:8].upper()


class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='employee_profile')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_employees')
    # integer employee id. Now enforce non-null and unique.
    employee_id = models.IntegerField(null=False, blank=False, unique=True)
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name