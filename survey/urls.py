from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.login_gateway, name='login_gateway'),
    path('admin_home/', views.index, name='admin_home'),
    path('employee/', views.employee, name='employee'),
    path('login/', views.login, name='login'),
    path('que_list/<int:survey_id>', views.question_list, name='que_list'),
    path('save/<int:survey_id>', views.save, name='save'),
    path('logout/', views.logout, name='logout'),
    url(r'^(?P<survey_id>[0-9]+)/assignSurvey/$', views.assign_survey, name='assignSurvey'),
    url(r'^(?P<survey_id>[0-9]+)/assignQuestion/$', views.assign_question, name='assignQuestion'),
    path('surveyList', views.survey_lists, name='surveyList'),
    path('saveAssignSurvey/', views.save_assign_survey, name='saveAssignSurvey'),
    path('saveAssignQuestion/', views.save_assign_question, name='saveAssignQuestion'),
    url(r'^(?P<survey_id>[0-9]+)/surveyQuest/$', views.survey_questions, name='surveyQuest'),
    path('report/', views.report, name='report')

]
