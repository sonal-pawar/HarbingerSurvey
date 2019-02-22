from django.contrib import admin
from .models import Employee, Organization,Survey,Question,SurveyEmployee, SurveyQuestion,SurveyFeedback
from django.conf import settings


class OrganizationDetails(admin.ModelAdmin):
    """
    This is organization model class for display table fields in tabular format and filter by city wise.
    """
    list_display = ('id', 'company_name', 'location', 'description', 'admin')
    list_filter = ('location',)


class EmployeeDetails(admin.ModelAdmin):
    """
    This is employee model class for display table fields in tabular format and filter by organization wise.
    """
    list_display = ('id', 'emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address', 'company')
    list_filter = ('company',)


class QuestionDetails(admin.ModelAdmin):
    """
    This is question model class for display table fields in tabular format and filter by survey, required,
    question type wise. The filter horizontal is used for display survey list in question form.
    """
    list_display = ('id', 'question', 'is_required', 'question_type', 'choices')
    list_filter = ('question',)


class SurveyDetails(admin.ModelAdmin):
    """
    This is survey model class for display table fields in tabular format and filter by employee, datetime wise.
    The filter horizontal is used for display employee list in survey form.
    """
    list_display = ('id', 'survey_name', 'description', 'date')
    list_filter = ('date',)


class AnswerDetails(admin.ModelAdmin):
    """
    This is answer model class for display table fields in tabular format and filter by employee, survey,
    created datetime, updated datetime wise.
    This model have only view permission
    """
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

