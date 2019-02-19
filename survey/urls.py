from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/', views.employee, name='employee'),
    path('login/', views.login, name='login'),
    path('que_list/<int:survey_id>', views.question_list, name='que_list'),
    path('save/<int:survey_id>', views.save, name='save'),
    path('logout/', views.logout, name='logout'),
    path('sendmail/', views.send_email, name='sendmail'),
    url(r'^(?P<survey_id>[0-9]+)/assignSurvey/$', views.assign_survey, name='assignSurvey'),
    path('surveyList', views.survey_lists, name='surveyList'),
    path('saveAssignSurvey/', views.save_assign_survey, name='saveAssignSurvey'),
    url(r'^(?P<survey_id>[0-9]+)/surveyQuest/$', views.survey_questions, name='surveyQuest'),
]
