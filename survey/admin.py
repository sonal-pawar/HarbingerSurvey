from django.contrib import admin
from .models import Employee, Organization,Survey,Question,SurveyEmployee, SurveyQuestion

admin.site.register(Employee)
admin.site.register(Organization)
admin.site.register(SurveyQuestion)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(SurveyEmployee)

