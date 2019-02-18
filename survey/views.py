from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, SurveyQuestion, Survey, SurveyEmployee, Question, SurveyFeedback
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'survey/home.html')


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
    print(question_data)

    ans_data = SurveyFeedback.objects.filter(survey_id=survey_id, employee_id=emp.id)

    for i in question_data:
        print(i.question_type)
    context = {'question_list': question_data, 'survey_id': survey_id, 'response': ans_data}
    return render(request, 'survey/question_list.html', context)


@login_required(login_url='login')
def employee(request):
    # survey details of logged in user displaying on this view
    if 'username' in request.session:
        m = request.session['username']
        emp = Employee.objects.get(emp_username=m)
        employee_data = Employee.objects.filter(id=emp.id)
        print(emp.id)
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

        assigned_survey_count = len(assigned_survey)
        completed_survey_count = len(completed_survey)
        context = {'session': m, 'survey_list': survey_emp_data, 'employee': employee_data,
                   'completed_survey': completed_survey, 'assigned_survey': assigned_survey,
                   'completed_survey_count': completed_survey_count,
                   'pending_survey_count': assigned_survey_count, 'incomplete_survey': incomplete_survey}
        print(survey_emp_data)

        return render(request, "survey/survey.html", context)
    return redirect('login')


def login(request):
    if request.method == "POST":
        print("Entering into post method")

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            if Employee.objects.get(emp_username=username, emp_password=password):
                m = request.session['username'] = username
                print("Session Name = "+m)
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
    print("current user", m)
    print("user id :", request.user.id)
    for name in request.POST:
        print("question id: ", name)
        all_answers = SurveyFeedback.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                 employee=Employee.objects.get(id=emp.id))
        if name != "csrfmiddlewaretoken" and name != 'btn_response':
            isRecord = SurveyFeedback.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                     employee=Employee.objects.get(id=emp.id),
                                                     question=Question.objects.get(id=name))
            if not isRecord:
                if request.POST[name]:
                    if request.POST.getlist(name):
                        surveyResultObj = SurveyFeedback()
                        surveyResultObj.survey = Survey.objects.get(id=survey_id)
                        print(surveyResultObj.survey)
                        surveyResultObj.employee = Employee.objects.get(id=emp.id)
                        print(surveyResultObj.employee)
                        surveyResultObj.question = Question.objects.get(id=name)
                        surveyResultObj.response = ', '.join(request.POST.getlist(name))
                        if request.POST["btn_response"] == "Finish":
                            surveyResultObj.flag = True
                        else:
                            surveyResultObj.flag = False
                        surveyResultObj.save()
        elif name == 'btn_response' and request.POST["btn_response"] == "Finish":
            for record in all_answers:
                record.flag = True
                record.save()
    return redirect("employee")


def send_email(request):
    try:
        name = request.session['username']
        print("Email has been send to :  ", name)
        email = EmailMessage('Survey Link', 'http://127.0.0.1:8000/employee/', to=[name])
        email.send()

        print("Email has been send to :  ", name)
        print("---------------mail sent---------------")
    except Exception as e:
        print(e)

    return redirect('employee')


def assign_survey(request, survey_id):
    user_list = Employee.objects.all()
    print(len(user_list))
    return render(request, 'survey/survey_assign.html', {"user_list": user_list, "survey_id": survey_id})


def save_assign_survey(request):
    if request.POST.getlist('emp_id'):
        for employee_id in request.POST.getlist('emp_id'):
            print("survey_id = ", request.POST['survey_id'])
            print("employee_id = ", employee_id)
            surveyEmployee = SurveyEmployee.objects.filter(survey_id=request.POST['survey_id'],
                                                           employee_id=employee_id)
            if not surveyEmployee:
                print(get_object_or_404(Employee, pk=employee_id))
                surveyEmployeeMapObj = SurveyEmployee()
                surveyEmployeeMapObj.survey = get_object_or_404(Survey, pk=request.POST['survey_id'])
                surveyEmployeeMapObj.employee = get_object_or_404(Employee, pk=employee_id)
                surveyEmployeeMapObj.save()
                userObj = get_object_or_404(Employee, pk=employee_id)
                print("User : ", userObj)
                to_email = userObj.emp_username
                print(to_email)
                try:
                    print("sed")
                    email_body = "http://127.0.0.1:8000/employee/"
                    email = EmailMessage(
                        'Survey Assign', email_body, to=[to_email]
                    )
                    email.send()
                except:
                    print("Email error")
                finally:
                    return redirect('surveyList')
    return redirect('surveyList')


def survey_lists(request):
    survey_list = Survey.objects.all()
    return render(request, 'survey/survey_employee.html', {"survey_list": survey_list})


def survey_questions(request, survey_id):
    survey_questions_list = SurveyQuestion.objects.filter(survey_id=survey_id)
    survey_employee_list = SurveyEmployee.objects.filter(survey_id=survey_id)
    return render(request, 'survey/survey_questions_list.html', {"survey_questions_list": survey_questions_list,
                                                                 "survey_employee_list": survey_employee_list})


