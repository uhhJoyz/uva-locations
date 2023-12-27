from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


class StudySpaces(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    noise_level = models.IntegerField(default=1)
    available_date = models.DateTimeField(default=timezone.now, blank=True)
    start_hours = models.TimeField(default=timezone.now, blank=True, null=True)
    end_hours = models.TimeField(default=timezone.now, blank=True, null=True)
    lat = models.FloatField(default=38.0312)
    lng = models.FloatField(default=-78.4989)
    reservation = models.BooleanField(default=False)
    location_details = models.CharField(max_length=255, null=True)
    amenities = models.CharField(max_length=255, null=True)
    maximum_occupancy = models.IntegerField(default=25, null=True)
    active = models.BooleanField(default=True)

    def is_available_now(self):
        return timezone.now() >= self.available_date

    def is_available_soon(self):
        return (
            timezone.now()
            <= self.available_date
            <= timezone.now() + datetime.timedelta(days=7)
        )


class Activities(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    date_time = models.DateTimeField(default=timezone.now, blank=True)
    lat = models.FloatField(default=38.0312)
    lng = models.FloatField(default=-78.4989)
    reservation = models.BooleanField(default=False)
    location_details = models.CharField(max_length=255, null=True)
    incentives = models.CharField(max_length=255, null=True)
    maximum_occupancy = models.IntegerField(default=25, null=True)
    active = models.BooleanField(default=True)

    def is_upcoming(self):
        return timezone.now() <= self.date_time

    def is_coming_soon(self):
        return (
            timezone.now()
            <= self.date_time
            <= timezone.now() + datetime.timedelta(days=7)
        )
