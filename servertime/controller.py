from datetime import datetime
from typing import Optional, Tuple
from servertime.models import Activity

TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%Y-%m-%d"


def _now_time():
    return datetime.now().strftime(TIME_FORMAT)


def _now_date():
    return datetime.now().strftime(DATE_FORMAT)


def _get_time_diff(beginning:str, end:str) -> Tuple[str, float]:
    t1 = datetime.strptime(beginning, TIME_FORMAT)
    t2 = datetime.strptime(end, TIME_FORMAT)
    delta = t2 - t1
    duration_seconds = delta.total_seconds()
    duration_hours = round((duration_seconds / 60) / 60, 2)
    return ':'.join(str(delta).split(':')[:2]), duration_hours


def _validate_date(date_text:str):
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        raise AssertionError(f"Incorrect data format, should be {DATE_FORMAT}")


def _validate_time(time_text:str):
    try:
        datetime.strptime(time_text, "%H:%M")
    except ValueError:
        raise AssertionError(f"Incorrect time format, should be {TIME_FORMAT}")


def finish_last_activity():
    today = datetime.now().strftime("%Y-%m-%d")
    # import pdb; pdb.set_trace()
    last_activity:Optional[dict] = Activity.find_last_of_date(today)

    if last_activity is None:
        return None

    updated_activity = None

    if last_activity.get("end") is None:
        update_fields = {}
        now_time = _now_time()
        update_fields["end"] = now_time
        update_fields["total"], update_fields["total_hours"] = _get_time_diff(last_activity["beginning"], now_time)
        updated_activity = Activity.update_activity(last_activity.get("_id"), update_fields)

    return updated_activity


def create_activity(name:str, description:str=""):
    # TODO: asserts

    finished_activity = finish_last_activity()

    activity = Activity(name=name, description=description)
    activity.save()

    return vars(activity), finished_activity


def get_activities(date:str):
    _validate_date(date)

    return Activity.find_by_date(date)


def update_activity(activity_id, update_fields):
    if "beginning" in update_fields.keys() and "end" in update_fields.keys():
        # import pdb; pdb.set_trace()
        update_fields["total"], update_fields["total_hours"] = _get_time_diff(update_fields["beginning"], update_fields["end"])

    updated_activity = Activity.update_activity(activity_id, update_fields)
    assert updated_activity is not None, f"Activity not found: {activity_id}"


    return updated_activity
