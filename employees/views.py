from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Max
from .models import Employee
from .forms import EmployeeForm
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views.generic import ListView


def home(request):
    # public homepage / landing
    return render(request, 'employees/home.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # allow login by email
        if user is None and '@' in username:
            try:
                u = User.objects.get(email=username)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is not None:
            login(request, user)
            return redirect('employees:list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'employees/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            last_id = Employee.objects.aggregate(Max('employee_id'))['employee_id__max'] or 1000
            Employee.objects.create(
                user=user,
                created_by=user,
                employee_id=int(last_id) + 1,
                full_name=user.username,
                email=user.email
            )
            messages.success(request, 'Account created. Please login.')
            return redirect('employees:login')
    else:
        form = RegistrationForm()
    return render(request, 'employees/register.html', {'form': form})


@login_required(login_url='employees:login')
def profile(request):
    # create employee if missing
    emp = getattr(request.user, 'employee_profile', None)
    if emp is None:
        last_id = Employee.objects.aggregate(Max('employee_id'))['employee_id__max'] or 1000
        emp = Employee.objects.create(
            user=request.user,
            created_by=request.user,
            employee_id=int(last_id) + 1,
            full_name=request.user.username,
            email=request.user.email
        )

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.user = request.user
            if emp.created_by is None:
                emp.created_by = request.user
            emp.save()
            messages.success(request, 'Profile saved')
            return redirect('employees:profile')
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'employees/profile.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('employees:login')


@login_required(login_url='employees:login')
def employee_list(request):
    q = request.GET.get('q', '').strip()
    if request.user.is_staff or request.user.is_superuser:
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(Q(created_by=request.user) | Q(user=request.user))
    if q:
        # if the query is numeric, allow searching by employee_id or primary key
        if q.isdigit():
            employees = employees.filter(
                Q(employee_id=int(q)) | Q(pk=int(q)) |
                Q(full_name__icontains=q) | Q(email__icontains=q) | Q(department__icontains=q)
            )
        else:
            employees = employees.filter(
                Q(full_name__icontains=q) |
                Q(email__icontains=q) |
                Q(department__icontains=q)
            )
    return render(request, 'employees/list.html', {'employees': employees, 'q': q})


@login_required(login_url='employees:login')
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.created_by = request.user
            if not emp.employee_id:
                last_id = Employee.objects.aggregate(Max('employee_id'))['employee_id__max'] or 1000
                emp.employee_id = int(last_id) + 1
            emp.save()
            return redirect('employees:list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Employee'})


class EmployeeListView(LoginRequiredMixin, ListView):
    login_url = 'employees:login'
    template_name = 'employees/cbv_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            qs = Employee.objects.all()
        else:
            qs = Employee.objects.filter(Q(created_by=self.request.user) | Q(user=self.request.user))
        q = self.request.GET.get('q', '').strip()
        if q:
            if q.isdigit():
                qs = qs.filter(
                    Q(employee_id=int(q)) | Q(pk=int(q)) |
                    Q(full_name__icontains=q) | Q(email__icontains=q) | Q(department__icontains=q)
                )
            else:
                qs = qs.filter(
                    Q(full_name__icontains=q) |
                    Q(email__icontains=q) |
                    Q(department__icontains=q)
                )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


@login_required(login_url='employees:login')
def employee_update(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if not (request.user.is_staff or request.user.is_superuser or emp.created_by == request.user or emp.user == request.user):
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employees:list')
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Employee'})


@login_required(login_url='employees:login')
def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if not (request.user.is_staff or request.user.is_superuser or emp.created_by == request.user or emp.user == request.user):
        return HttpResponseForbidden('Not allowed')
    return render(request, 'employees/detail.html', {'employee': emp})


@login_required(login_url='employees:login')
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if not (request.user.is_staff or request.user.is_superuser or emp.created_by == request.user or emp.user == request.user):
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        emp.delete()
        return redirect('employees:list')
    return render(request, 'employees/confirm_delete.html', {'employee': emp})
