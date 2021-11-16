import datetime
from typing import Optional
from servertime.models import Activity


def _validate_date(date_text:str):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise AssertionError("Incorrect data format, should be YYYY-MM-DD")


def _validate_time(time_text:str):
    try:
        datetime.datetime.strptime(time_text, "%H:%M")
    except ValueError:
        raise AssertionError("Incorrect data format, should be YYYY-MM-DD")


def create_activity(name:str, description:str=""):
    # TODO: asserts

    activity = Activity(name=name, description=description)
    activity.save()
    return vars(activity)


def get_activities(date:str):
    _validate_date(date)

    return Activity.find_by_date(date)
