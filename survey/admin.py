from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Organization, Survey, Question, SurveyEmployee, SurveyQuestion, SurveyFeedback, User


class UserResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('id', 'emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address', 'organization')
        export_order = fields
        skip_unchanged = True
        report_skipped = True


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = SurveyEmployee
        fields = ('id', 'survey', 'employee', 'startDatetime', 'endDatetime', 'flag')
        export_order = fields


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


class EmployeeDetails(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'emp_name', 'emp_username', 'emp_designation', 'emp_address', 'organization')
    list_filter = ('emp_username',)
    fieldsets = (
        ('Personal info', {'fields': ('emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('emp_name', 'emp_username', 'emp_password', 'emp_designation', 'emp_address')}),
    )
    ordering = ('emp_username',)
    resource_class = UserResource

    def get_queryset(self, request):
        qs = super(EmployeeDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization_id=request.user.organization)
        return qs

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
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
    ordering = ('date',)

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
    list_display = ('id', 'survey', 'question')
    list_filter = ('question',)
    fieldsets = (
        ('survey', {'fields': ('survey', 'question')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('survey', {'fields': ('survey', 'question')}),
    )
    ordering = ('survey',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(organization=request.user.organization)
        if db_field.name == 'survey':
            kwargs["queryset"] = Survey.objects.filter(organization=request.user.organization)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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


class SurveyEmployeeDetails(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'survey', 'employee', 'startDatetime', 'endDatetime', 'status_list')
    list_filter = ('survey',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = Employee.objects.filter(organization=request.user.organization)
        if db_field.name == 'survey':
            kwargs["queryset"] = Survey.objects.filter(organization=request.user.organization)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('survey', {'fields': ('survey', 'employee', 'startDatetime', 'endDatetime')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('survey', {'fields': ('survey', 'employee', 'startDatetime', 'endDatetime')}),
    )
    ordering = ('survey',)
    resource_class = EmployeeResource

    def status_list(self, obj):
        if obj.flag is True:
            return 'Completed'
        elif obj.flag is False:
            return 'Pending'
        elif obj.flag is None:
            return "Not started"
    status_list.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.flag = None
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyEmployeeDetails, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(organization=request.user.organization)
        return qs


class AnswerDetails(admin.ModelAdmin):

    list_display = ('id', 'employee', 'survey', 'question', 'organization', 'response',
                    'flag', 'created_date', 'updated_date')
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
