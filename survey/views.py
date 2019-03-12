import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.core.mail import EmailMessage
from smtplib import SMTPAuthenticationError
from .models import Employee, SurveyQuestion, Survey, SurveyEmployee, Question, SurveyFeedback, User

logger = logging.getLogger(__name__)


@login_required(login_url='admin:index')
def index(request):
    if request.user.is_authenticated:
        logger.warning(" Admin must be authenticated ")
        user_data = User.objects.filter(organization_id=request.user.organization_id)
        logger.info("Now {} is logged in ".format(request.user))
        context = {'user_data': user_data}
        return render(request, 'survey/home.html', context)


def question_list(request, survey_id):
    # This view Displaying survey questions of particular survey
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)
    survey_data = SurveyQuestion.objects.filter(survey=survey_id).values('question')
    count = 0
    que_id1 = ()
    for questions in survey_data:
        print(questions)
        que_id = survey_data[count]['question']
        que_id1 += (que_id,)
        count += 1

    question_data = Question.objects.filter(id__in=que_id1)
    ans_data = SurveyFeedback.objects.filter(survey_id=survey_id, employee_id=emp.id)
    context = {'question_list': question_data, 'survey_id': survey_id, 'response': ans_data}
    return render(request, 'survey/question_list.html', context)


@login_required(login_url='login')
def employee(request):
    # survey details of logged in user displaying on this view
    if 'username' in request.session:
        m = request.session['username']
        emp = Employee.objects.get(emp_username=m)
        employee_data = Employee.objects.filter(id=emp.id)
        survey_emp_data = SurveyEmployee.objects.filter(employee=emp.id, startDatetime__lte=now(),
                                                        endDatetime__gte=now())
        upcoming_surveys = SurveyEmployee.objects.filter(employee=emp.id, startDatetime__gt=now(),
                                                         endDatetime__gte=now())
        expired_surveys = SurveyEmployee.objects.filter(employee=emp.id, startDatetime__lt=now(),
                                                        endDatetime__lte=now())
        current_surveys = SurveyEmployee.objects.filter(employee=emp.id, startDatetime__lte=now(),
                                                        endDatetime__gte=now())
        completed_survey = list()
        assigned_survey = list()
        incomplete_survey = list()

        for survey in survey_emp_data:
            survey_feedback = SurveyFeedback.objects.filter(employee_id=emp.id, survey_id=survey.survey_id).count()
            if survey_feedback:
                if SurveyFeedback.objects.filter(survey_id=survey.survey_id, employee_id=emp.id, flag=True):
                    completed_survey.append(survey)
                else:
                    incomplete_survey.append(survey)
            else:
                assigned_survey.append(survey)

        pending_survey_count = len(assigned_survey)
        completed_survey_count = len(completed_survey)
        context = {'session': m, 'survey_list': survey_emp_data, 'employee': employee_data,
                   'completed_survey': completed_survey, 'assigned_survey': assigned_survey,
                   'upcoming_surveys': upcoming_surveys, 'expired_surveys': expired_surveys,
                   'current_surveys': current_surveys,
                   'completed_survey_count': completed_survey_count,
                   'pending_survey_count': pending_survey_count, 'incomplete_survey': incomplete_survey}
        return render(request, "survey/survey.html", context)
    return redirect('login')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            if Employee.objects.get(emp_username=username, emp_password=password):
                request.session['username'] = username

                return redirect('employee')
        except BaseException as e:
            print(e)
            return render(request, "survey/login.html")
    return render(request, "survey/login.html")


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')


def save(request, survey_id):
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)
    for name in request.POST:
        all_answers = SurveyFeedback.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                    employee=Employee.objects.get(id=emp.id))

        if name != "csrfmiddlewaretoken" and name != 'btn_response':
            is_record = SurveyFeedback.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                      employee=Employee.objects.get(id=emp.id),
                                                      question=Question.objects.get(id=name))
            if not is_record:
                if request.POST[name]:
                    if request.POST.getlist(name):
                        survey_result_obj = SurveyFeedback()
                        survey_result_obj.survey = Survey.objects.get(id=survey_id)
                        survey_result_obj.employee = Employee.objects.get(id=emp.id)
                        survey_result_obj.question = Question.objects.get(id=name)
                        survey_result_obj.organization = request.user.organization
                        survey_result_obj.response = ', '.join(request.POST.getlist(name))
                        survey_status = SurveyEmployee.objects.get(employee=Employee.objects.get(id=emp.id),
                                                                   survey=Survey.objects.get(id=survey_id),
                                                                   organization=request.user.organization)
                        if request.POST["btn_response"] == "Finish":
                            survey_result_obj.flag = True
                            survey_result_obj.save()
                            survey_status.flag = True
                            survey_status.save()

                        else:
                            survey_result_obj.flag = False
                            survey_result_obj.save()
                            survey_status.flag = False
                            survey_status.save()
        elif name == 'btn_response' and request.POST["btn_response"] == "Finish":

            for record in all_answers:
                record.flag = True
                record.save()
            try:
                email_body = "Hi, \n Your have completed the survey \n" + \
                             request.build_absolute_uri('/')[:-1].strip("/") \
                             + "/employee"
                email = EmailMessage(
                    'Survey Feedback ', email_body, to=[m]
                )
                # email.send()
                print("Email has been send to ", m)
            except SMTPAuthenticationError as e:
                print("Email Error : ", e)

    return redirect("employee")


def assign_survey(request, survey_id):
    user_list = Employee.objects.filter(organization_id=request.user.organization)
    return render(request, 'survey/survey_assign.html', {"user_list": user_list, "survey_id": survey_id})


def assign_question(request, survey_id):
    questions = Question.objects.filter(organization=request.user.organization)
    return render(request, 'survey/question_assign.html', {"question_list": questions, "survey_id": survey_id})


def save_assign_survey(request):
    if request.POST.getlist('emp_id'):
        for name in request.POST:
            print(name)
        for employee_id in request.POST.getlist('emp_id'):
            survey_employee = SurveyEmployee.objects.filter(survey_id=request.POST['survey_id'],
                                                            employee_id=employee_id)
            if not survey_employee:
                survey_employee_map_obj = SurveyEmployee()
                survey_employee_map_obj.survey = get_object_or_404(Survey, pk=request.POST['survey_id'])
                survey_employee_map_obj.employee = get_object_or_404(Employee, pk=employee_id)
                survey_employee_map_obj.organization = request.user.organization
                survey_employee_map_obj.startDatetime = parse_date(request.POST.getlist('start-date')[1])
                print("date : ", survey_employee_map_obj.startDatetime)

                survey_employee_map_obj.endDatetime = parse_date(request.POST.getlist('end-date')[1])

                survey_employee_map_obj.save()
                user_obj = get_object_or_404(Employee, pk=employee_id)
                to_email = user_obj.emp_username
                try:
                    email_body = "Hi, \n Your Survey Link\n" + request.build_absolute_uri('/')[:-1].strip("/")\
                                 + "/employee"
                    email = EmailMessage(
                        'Survey Assign', email_body, to=[to_email]
                    )
                    # email.send()
                    print("Email has been send to ", to_email)
                except SMTPAuthenticationError as e:
                    print("Email Error : ", e)
                finally:
                    return redirect('surveyList')
    return redirect('surveyList')


def save_assign_question(request):
    if request.POST.getlist('question_id'):
        for question_id in request.POST.getlist('question_id'):
            survey_question = SurveyQuestion.objects.filter(survey_id=request.POST['survey_id'],
                                                            question_id=question_id)
            if not survey_question:
                survey_question_map_obj = SurveyQuestion()
                survey_question_map_obj.survey = get_object_or_404(Survey, pk=request.POST['survey_id'])
                survey_question_map_obj.organization = request.user.organization
                survey_question_map_obj.question = get_object_or_404(Question, pk=question_id)
                survey_question_map_obj.save()
    return redirect('surveyList')


def survey_lists(request):
    survey_list = Survey.objects.filter(organization=request.user.organization)
    return render(request, 'survey/survey_employee.html', {"survey_list": survey_list})


def survey_questions(request, survey_id):
    survey_questions_list = SurveyQuestion.objects.filter(survey_id=survey_id,
                                                          organization=request.user.organization)
    survey_employee_list = SurveyEmployee.objects.filter(survey_id=survey_id,
                                                         organization=request.user.organization)
    return render(request, 'survey/survey_questions_list.html', {"survey_questions_list": survey_questions_list,
                                                                 "survey_employee_list": survey_employee_list})


def report(request):
    survey_data = SurveyEmployee.objects.filter(organization_id=request.user.organization)
    context = {'survey': survey_data}
    return render(request, 'survey/report.html', context)


