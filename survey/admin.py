from django.contrib import admin
from .models import Employee, Organization,Survey,Question,SurveyEmployee, SurveyQuestion, SurveyFeedback, User
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'organization')
        export_order = ('username', 'first_name', 'email', 'organization')
        skip_unchanged = True
        report_skipped = False


class MyUserAdmin(UserAdmin, ImportExportModelAdmin):
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
    resource_class = UserResource


class OrganizationDetails(admin.ModelAdmin):

    list_display = ('id', 'company_name', 'location', 'description')
    list_filter = ('location',)


class EmployeeDetails(admin.ModelAdmin):
    list_display = ('id', 'emp_name', 'emp_username', 'emp_designation', 'emp_address', 'company')
    # list_filter = ('company',)
    fieldsets = (
        ('Personal info', {'fields': ('emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address')}),
    )
    ordering = ('emp_username',)

    def get_queryset(self, request):
        qs = super(EmployeeDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(company=request.user.organization)
        return qs

    def save_model(self, request, obj, form, change):
        obj.company = request.user.organization
        obj.save()


class QuestionDetails(admin.ModelAdmin):

    list_display = ('id', 'question', 'question_type', 'choices')
    list_filter = ('question',)

    fieldsets = (
        ('questions', {'fields': ('question', 'question_type', 'choices')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('questions', {'fields':  ('question', 'question_type', 'choices')}),
    )
    ordering = ('question',)

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.save()

    def get_queryset(self, request):
        qs = super(QuestionDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization=request.user.organization)
        return qs


class SurveyDetails(admin.ModelAdmin):

    list_display = ('id', 'survey_name', 'description', 'date')
    list_filter = ('date',)

    fieldsets = (
        ('Survey', {'fields': ('survey_name', 'description', 'date')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Survey', {'fields': ('survey_name', 'description', 'date')}),
    )
    ordering = ('survey_name',)

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization=request.user.organization)
        return qs


class SurveyQuestionDetails(admin.ModelAdmin):
    list_display = ('id', 'survey')
    list_filter = ('question',)
    fieldsets = (
        ('survey', {'fields': ('survey', 'question')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('survey', {'fields': ('survey', 'question')}),
    )
    ordering = ('survey',)

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyQuestionDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization=request.user.organization)
        return qs


class SurveyEmployeeDetails(admin.ModelAdmin):
    list_display = ('id', 'survey', 'employee', 'organization')
    list_filter = ('survey',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = Employee.objects.filter(company=request.user.organization)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('survey', {'fields': ('survey', 'employee', 'startDatetime', 'endDatetime')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('survey', {'fields': ('survey', 'employee', 'startDatetime', 'endDatetime')}),
    )
    ordering = ('survey',)

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyEmployeeDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization=request.user.organization)
        return qs


class AnswerDetails(admin.ModelAdmin):

    list_display = ('id', 'employee', 'survey', 'question', 'organization', 'response', 'flag', 'created_date', 'updated_date')
    list_filter = ('employee', 'survey', 'created_date', 'updated_date')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.save()

    def get_queryset(self, request):
        qs = super(AnswerDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization=request.user.organization)
        return qs


admin.site.register(Employee, EmployeeDetails)
admin.site.register(Organization, OrganizationDetails)
admin.site.register(SurveyQuestion, SurveyQuestionDetails)
admin.site.register(Question, QuestionDetails)
admin.site.register(Survey, SurveyDetails)
admin.site.register(SurveyEmployee, SurveyEmployeeDetails)
admin.site.register(SurveyFeedback, AnswerDetails)
admin.site.register(User, MyUserAdmin)

admin.site.site_header = 'Survey Administration'
admin.site.site_title = "Survey Admin Portal"
admin.site.index_title = "Welcome to Survey Admin Portal"
