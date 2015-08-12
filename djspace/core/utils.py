from django.conf import settings
from djtools.fields import NOW
from datetime import datetime

def get_profile_status(user):
    """
    simple function that compares the user's profile updated datetime
    against the grant cycle start date, which is comprised of the
    current year and the settings value for the month and the first
    day of the month.
    """
    grant_cycle_start_date = datetime(
        NOW.year, settings.GRANT_CYCLE_START_MES, 1
    )
    status = False
    if user.profile.date_updated > grant_cycle_start_date:
        status = True
    return status