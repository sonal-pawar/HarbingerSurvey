from django.contrib import admin
from .models import Employee, Organization,Survey,Question,SurveyEmployee, SurveyQuestion, SurveyFeedback, User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'first_name', 'email', 'organization']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'organization',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'organization',)}),
    )
    ordering = ('username',)


class OrganizationDetails(admin.ModelAdmin):

    list_display = ('id', 'company_name', 'location', 'description')
    list_filter = ('location',)


class EmployeeDetails(admin.ModelAdmin):

    list_display = ('id', 'emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address', 'company')
    list_filter = ('company',)


class QuestionDetails(admin.ModelAdmin):

    list_display = ('id', 'question', 'is_required', 'question_type', 'choices')
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


admin.site.register(Employee, EmployeeDetails)
admin.site.register(Organization, OrganizationDetails)
admin.site.register(SurveyQuestion)
admin.site.register(Question, QuestionDetails)
admin.site.register(Survey, SurveyDetails)
admin.site.register(SurveyEmployee)
admin.site.register(SurveyFeedback, AnswerDetails)
admin.site.register(User, MyUserAdmin)

