from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, SurveyQuestion, Survey, SurveyEmployee, Question, SurveyFeedback, User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


@login_required(login_url='admin:index')
def index(request):
    if request.user.is_authenticated:
        user_data = User.objects.filter(organization_id=request.user.organization_id)
        context = {'user_data': user_data}
        return render(request, 'survey/home.html', context)


@login_required(login_url='admin:index')
def question_list(request, survey_id):
    # This view Displaying survey questions of particular survey
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)
    survey_data = SurveyQuestion.objects.filter(survey=survey_id).values('question')
    j = 0
    que_id1 = ()
    for i in survey_data:
        print(i)
        que_id = survey_data[j]['question']
        que_id1 += (que_id,)
        j += 1

    question_data = Question.objects.filter(id__in=que_id1)
    ans_data = SurveyFeedback.objects.filter(survey_id=survey_id, employee_id=emp.id)
    context = {'question_list': question_data, 'survey_id': survey_id, 'response': ans_data}
    return render(request, 'survey/question_list.html', context)


@login_required(login_url='login')
@login_required(login_url='admin:index')
def employee(request):
    # survey details of logged in user displaying on this view
    if 'username' in request.session:
        m = request.session['username']
        emp = Employee.objects.get(emp_username=m)
        employee_data = Employee.objects.filter(id=emp.id)
        survey_emp_data = SurveyEmployee.objects.filter(employee=emp.id)

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
                   'completed_survey_count': completed_survey_count,
                   'pending_survey_count': pending_survey_count, 'incomplete_survey': incomplete_survey}
        return render(request, "survey/survey.html", context)
    return redirect('login')


@login_required(login_url='admin:index')
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


@login_required(login_url='admin:index')
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
                        survey_result_obj.response = ', '.join(request.POST.getlist(name))
                        if request.POST["btn_response"] == "Finish":
                            survey_result_obj.flag = True
                            survey_result_obj.save()

                        else:
                            survey_result_obj.flag = False
                            survey_result_obj.save()
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
                email.send()
                print("Email has been send to ", m)
            except Exception as e:
                print("Email Error : ", e)

    return redirect("employee")


@login_required(login_url='admin:index')
def assign_survey(request, survey_id):
    user_list = Employee.objects.all()
    return render(request, 'survey/survey_assign.html', {"user_list": user_list, "survey_id": survey_id})


@login_required(login_url='admin:index')
def save_assign_survey(request):
    if request.POST.getlist('emp_id'):
        for employee_id in request.POST.getlist('emp_id'):
            survey_employee = SurveyEmployee.objects.filter(survey_id=request.POST['survey_id'],
                                                            employee_id=employee_id)
            if not survey_employee:
                survey_employee_map_obj = SurveyEmployee()
                survey_employee_map_obj.survey = get_object_or_404(Survey, pk=request.POST['survey_id'])
                survey_employee_map_obj.employee = get_object_or_404(Employee, pk=employee_id)
                survey_employee_map_obj.save()
                user_obj = get_object_or_404(Employee, pk=employee_id)
                to_email = user_obj.emp_username
                try:
                    email_body = "Hi, \n Your Survey Link\n" + request.build_absolute_uri('/')[:-1].strip("/")\
                                 + "/employee"
                    email = EmailMessage(
                        'Survey Assign', email_body, to=[to_email]
                    )
                    email.send()
                    print("Email has been send to ", to_email)
                except Exception as e:
                    print("Email Error : ", e)
                finally:
                    return redirect('surveyList')
    return redirect('surveyList')


@login_required(login_url='admin:index')
def survey_lists(request):
    survey_list = Survey.objects.all()
    return render(request, 'survey/survey_employee.html', {"survey_list": survey_list})


@login_required(login_url='admin:index')
def survey_questions(request, survey_id):
    survey_questions_list = SurveyQuestion.objects.filter(survey_id=survey_id)
    survey_employee_list = SurveyEmployee.objects.filter(survey_id=survey_id)
    return render(request, 'survey/survey_questions_list.html', {"survey_questions_list": survey_questions_list,
                                                                 "survey_employee_list": survey_employee_list})
