from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from SurveyUpdater import survey_api
from survey.models import User, Employee, Survey, SurveyFeedback, SurveyQuestion


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(survey_api.send_email, 'interval', minutes=5)
    scheduler.start()
