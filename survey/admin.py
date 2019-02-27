from django.contrib import admin
from .models import Employee, Organization,Survey,Question,SurveyEmployee, SurveyQuestion, SurveyFeedback, User, Report
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'first_name', 'email', 'organization']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'organization', 'groups')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'organization', 'groups')}),
    )
    ordering = ('username',)


class OrganizationDetails(admin.ModelAdmin):

    list_display = ('id', 'company_name', 'location', 'description')
    list_filter = ('location',)


class EmployeeDetails(admin.ModelAdmin):
    list_display = ('id', 'emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address', 'company')
    list_filter = ('company',)
    fieldsets = (
        ('Personal info', {'fields': ('emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address')}),
    )
    ordering = ('emp_username',)

    def save_model(self, request, obj, form, change):
        obj.company = request.user.organization
        obj.save()


class QuestionDetails(admin.ModelAdmin):

    list_display = ('id', 'question', 'question_type', 'choices')
    list_filter = ('question',)


class SurveyDetails(admin.ModelAdmin):

    list_display = ('id', 'survey_name', 'description', 'date')
    list_filter = ('date',)


class AnswerDetails(admin.ModelAdmin):

    list_display = ('id', 'employee', 'survey', 'question', 'response', 'flag', 'created_date', 'updated_date')
    list_filter = ('employee', 'survey', 'created_date', 'updated_date')

    # This function will be disable add permission for answer model
    def has_add_permission(self, request, obj=None):
        return False

    # This function will be disable change permission for answer model
    def has_change_permission(self, request, obj=None):
        return False

    # This function will be disable delete permission for answer model
    def has_delete_permission(self, request, obj=None):
        return False


class ReportDetails(admin.ModelAdmin):
    list_display = ('id', 'employee', 'SurveyFeedback', 'Survey')
    list_filter = ('employee', 'SurveyFeedback', 'Survey')

    # This function will be disable add permission for answer model
    def has_add_permission(self, request, obj=None):
        return False

    # This function will be disable change permission for answer model
    def has_change_permission(self, request, obj=None):
        return False

    # This function will be disable delete permission for answer model
    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        user = request.user.organization
        obj.employee = Employee.objects.get(company=user)
        obj.SurveyFeedback = SurveyFeedback.objects.get(employee_id=obj.employee.id)
        obj.save()


admin.site.register(Employee, EmployeeDetails)
admin.site.register(Organization, OrganizationDetails)
admin.site.register(SurveyQuestion)
admin.site.register(Question, QuestionDetails)
admin.site.register(Survey, SurveyDetails)
admin.site.register(SurveyEmployee)
admin.site.register(SurveyFeedback, AnswerDetails)
admin.site.register(User, MyUserAdmin)
admin.site.register(Report, ReportDetails)

admin.site.site_header = 'Survey Administration'
admin.site.site_title = "Survey Admin Portal"
admin.site.index_title = "Welcome to Survey Admin Portal"
