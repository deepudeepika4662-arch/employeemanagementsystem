from django.contrib import admin
from django.db.models import Max
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'employee_id', 'full_name', 'email', 'department', 'age', 'created_by', 'user'
    )
    list_display_links = ('id', 'full_name')
    list_editable = ('department', 'age')
    search_fields = ('employee_id', 'full_name', 'email', 'department')
    list_filter = ('department', 'created_by', 'user')
    ordering = ('employee_id',)
    list_per_page = 50
    list_select_related = ('created_by', 'user')
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('employee_id', 'full_name', 'email', 'department', 'age')
        }),
        ('User settings', {
            'fields': ('user', 'created_by')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('id', 'employee_id')
        return ('id',)

    def save_model(self, request, obj, form, change):
        if not obj.employee_id:
            last_id = Employee.objects.aggregate(Max('employee_id'))['employee_id__max'] or 1000
            obj.employee_id = int(last_id) + 1
        super().save_model(request, obj, form, change)
