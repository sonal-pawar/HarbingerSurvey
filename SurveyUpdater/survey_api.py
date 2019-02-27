import requests
from survey.models import User, Employee, Survey, SurveyFeedback, SurveyQuestion
import survey.views
from django.core.mail import EmailMessage


def send_email(request):
    user_list = Employee.objects.all()
    to_email = user_list.emp_username
    try:
        email_body = "Hi, \n Your Survey Link\n" + request.build_absolute_uri('/')[:-1].strip("/") \
                     + "/employee"
        email = EmailMessage(
            'Survey Assign', email_body, to=[to_email]
        )
        email.send()
        print("Email has been send to ", to_email)
    except Exception as e:
        print("Email Error : ", e)
    finally:
        return None
