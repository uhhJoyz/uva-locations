from locations.models import StudySpaces, Activities
from django.utils import timezone
import datetime


def create_StudySpace(
    location,
    name,
    is_verified,
    days=0,
    noise_level=1,
    reservation=True,
    location_details=any,
    amenities=any,
    active=True,
):
    time = timezone.now() + datetime.timedelta(days=days)
    return StudySpaces.objects.create(
        location=location,
        name=name,
        is_verified=is_verified,
        available_date=time,
        noise_level=noise_level,
        reservation=reservation,
        location_details=location_details,
        amenities=amenities,
        active=active,
    )


def create_Activities(
    location,
    name,
    is_verified,
    days=0,
    reservation=True,
    location_details=any,
    incentives=any,
    active=True,
):
    time = timezone.now() + datetime.timedelta(days=days)
    return Activities.objects.create(
        location=location,
        name=name,
        is_verified=is_verified,
        date_time=time,
        reservation=reservation,
        location_details=location_details,
        incentives=incentives,
        active=active,
    )
