import json

import datetime
from time import strftime

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
from django.views import generic
from .models import StudySpaces, Activities
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

cur_space_key = "is_verified"
cur_activities_key = "is_verified"

cur_index_space = "is_verified"
cur_index_activities = "is_verified"


class IndexView(TemplateView):
    template_name = "locations/index.html"


class VerifyView(TemplateView):
    template_name = "locations/verification.html"


class AdminHomepage(TemplateView):
    template_name = "locations/admin.html"


class AddActivityView(TemplateView):
    template_name = "locations/add_activity.html"


class AddStudySpaceView(TemplateView):
    template_name = "locations/add_study_space.html"


class DeleteView(TemplateView):
    template_name = "locations/delete.html"


def admin_homepage(request):
    global cur_activities_key, cur_space_key

    if not request.user.is_staff:
        return redirect("locations:index")

    study_spaces = StudySpaces.objects.filter(is_verified=True, active=True)
    activities = Activities.objects.filter(
        date_time__gte=timezone.now(), is_verified=True, active=True
    )

    if request.method == "POST":
        # when sorting study spaces
        space_key = request.POST.get("space_key")
        if space_key == "spaces_by_name":
            cur_space_key = "name"
        elif space_key == "spaces_by_location":
            cur_space_key = "location"
        elif space_key == "reset":
            cur_space_key = "is_verified"
        elif space_key == "spaces_by_noise_level":
            cur_space_key = "noise_level"

        # when sorting activities
        activity_key = request.POST.get("activity_key")
        if activity_key == "activities_by_name":
            cur_activities_key = "name"
        elif activity_key == "activities_by_location":
            cur_activities_key = "location"
        elif activity_key == "activities_by_date":
            cur_activities_key = "date_time"
        elif activity_key == "reset":
            cur_activities_key = "is_verified"
        elif activity_key == "activities_by_noise_level":
            cur_activities_key = "noise_level"

        displayed_spaces = study_spaces.order_by(cur_space_key)
        displayed_activities = activities.order_by(cur_activities_key)

    else:
        displayed_spaces = study_spaces.order_by("name")
        displayed_activities = activities.order_by("name")

    context = {
        "study_spaces": study_spaces,
        "activities": activities,
        "displayed_spaces": displayed_spaces,
        "displayed_activities": displayed_activities,
        "prev_act_key": cur_index_activities
        if cur_index_activities
        else "activities_by_name",
        "prev_space_key": cur_index_space if cur_index_space else "spaces_by_name",
    }

    return render(request, "locations/admin.html", context)


# Create your views here.
def index(request):
    global cur_index_space, cur_index_activities
    if not request.user.is_authenticated:
        return redirect("accounts/google/login")

    if request.user.is_authenticated and (
        request.user.email == "cs3240.super@gmail.com"
        or request.user.email == "wcb8ze@virginia.edu"
    ):
        request.user.is_staff = True
        request.user.save()

        return redirect("locations:admin_home")

    if request.user.is_staff:
        return redirect("locations:admin_home")

    study_spaces = StudySpaces.objects.filter(is_verified=True, active=True)
    activities = Activities.objects.filter(
        date_time__gte=timezone.now(), is_verified=True, active=True
    )

    if request.method == "POST":
        # when sorting study spaces
        space_key = request.POST.get("space_key")
        if space_key == "spaces_by_name":
            cur_index_space = "name"
        elif space_key == "spaces_by_location":
            cur_index_space = "location"
        elif space_key == "reset":
            cur_index_space = "is_verified"
        elif space_key == "spaces_by_noise_level":
            cur_index_space = "noise_level"

        # when sorting activities
        activity_key = request.POST.get("activity_key")
        if activity_key == "activities_by_name":
            cur_index_activities = "name"
        elif activity_key == "activities_by_location":
            cur_index_activities = "location"
        elif activity_key == "activities_by_date":
            cur_index_activities = "date_time"
        elif activity_key == "reset":
            cur_index_activities = "is_verified"
        elif activity_key == "activities_by_noise_level":
            cur_index_activities = "noise_level"

        displayed_spaces = study_spaces.order_by(cur_index_space)
        displayed_activities = activities.order_by(cur_index_activities)

    else:
        displayed_spaces = study_spaces.order_by("name")
        displayed_activities = activities.order_by("name")

    context = {
        "study_spaces": study_spaces,
        "activities": activities,
        "displayed_spaces": displayed_spaces,
        "displayed_activities": displayed_activities,
        "prev_act_key": cur_index_activities
        if cur_index_activities
        else "activities_by_name",
        "prev_space_key": cur_index_space if cur_index_space else "spaces_by_name",
    }

    return render(request, "locations/index.html", context)


def verify(request):
    if request.method == "POST":
        study_space_ids = request.POST.getlist("study_spaces")
        activity_ids = request.POST.getlist("activities")

        for spot_id in study_space_ids:
            spot = StudySpaces.objects.get(pk=spot_id)
            spot.is_verified = True
            spot.save()

        for activity_id in activity_ids:
            activity = Activities.objects.get(pk=activity_id)
            activity.is_verified = True
            activity.save()

    unverified_spots_list = StudySpaces.objects.filter(is_verified=False, active=True)
    unverified_activities_list = Activities.objects.filter(
        is_verified=False, active=True
    )

    context = {
        "unverified_spots_list": unverified_spots_list,
        "unverified_activities_list": unverified_activities_list,
    }

    return render(request, "locations/verification.html", context)


def delete(request):
    author = request.user
    if request.method == "POST":
        study_space_ids = request.POST.getlist("study_spaces")
        activity_ids = request.POST.getlist("activities")

        for spot_id in study_space_ids:
            spot = StudySpaces.objects.get(pk=spot_id)
            spot.active = False
            spot.save()

        for activity_id in activity_ids:
            activity = Activities.objects.get(pk=activity_id)
            activity.active = False
            activity.save()

    user_spots = StudySpaces.objects.filter(author=author, active=True)
    user_activities = Activities.objects.filter(author=author, active=True)
    if request.user.is_staff:
        user_spots = StudySpaces.objects.filter(active=True)
        user_activities = Activities.objects.filter(active=True)

    context = {
        "unverified_spots_list": user_spots,
        "unverified_activities_list": user_activities,
    }

    return render(request, "locations/delete.html", context)


def add_activity(request):
    if request.method == "POST":
        new_name = request.POST.get("a_name")
        new_loc = request.POST.get("l_name")
        new_time = request.POST.get("activity_time")
        new_lat = request.POST.get("lat")
        new_lng = request.POST.get("lng")
        new_reservation = request.POST.getlist("reservation")
        new_loc_info = request.POST.get("location_details")
        new_incentives = request.POST.get("incentives")
        new_max_occ = request.POST.get("maximum_occupancy")

        if (
            len(new_name.strip()) != 0
            and len(new_loc.strip()) != 0
            and len(new_time) != 0
        ):
            activity = Activities(
                author=request.user,
                name=new_name,
                location=new_loc,
                is_verified=False,
                date_time=new_time,
                lat=new_lat,
                lng=new_lng,
                reservation=True if len(new_reservation) > 0 else False,
                location_details=new_loc_info,
                incentives=new_incentives,
                maximum_occupancy=new_max_occ,
            )
            activity.save()
            return redirect("locations:index")
        else:
            return render(
                request,
                "locations/add_activity.html",
                {
                    "error_message": "Please fill out all of the input fields.",
                    "api_key": settings.GOOGLE_API_KEY,
                },
            )
    else:
        context = {"api_key": settings.GOOGLE_API_KEY}
        return render(request, "locations/add_activity.html", context=context)


def add_study_space(request):
    if request.method == "POST":
        new_name = request.POST.get("a_name")
        new_loc = request.POST.get("l_name")
        new_noise = request.POST.get("noise_level")
        new_start_hours = request.POST.get("start_hours")
        new_end_hours = request.POST.get("end_hours")
        new_lat = request.POST.get("lat")
        new_lng = request.POST.get("lng")
        new_reservation = request.POST.getlist("reservation")
        new_loc_info = request.POST.get("location_details")
        new_amenities = request.POST.get("amenities")
        new_max_occ = request.POST.get("maximum_occupancy")

        if len(new_name.strip()) != 0 and len(new_loc.strip()) != 0:
            # correct noise level if out of bounds
            if new_noise:
                new_noise = int(new_noise)
            if new_noise and (5 < new_noise or new_noise < 1):
                new_noise = min(max(new_noise, 1), 5)
            space = StudySpaces(
                author=request.user,
                name=new_name,
                location=new_loc,
                is_verified=False,
                noise_level=int(new_noise) if new_noise else 3,
                start_hours=new_start_hours,
                end_hours=new_end_hours,
                lat=new_lat,
                lng=new_lng,
                location_details=new_loc_info,
                reservation=True if len(new_reservation) > 0 else False,
                amenities=new_amenities,
                maximum_occupancy=new_max_occ,
            )
            space.save()
            return redirect("locations:index")
        else:
            return render(
                request,
                "locations/add_study_space.html",
                {
                    "error_message": "Please fill out all of the input fields.",
                    "api_key": settings.GOOGLE_API_KEY,
                },
            )
    else:
        # TODO: setup api key in environment variable
        context = {"api_key": settings.GOOGLE_API_KEY}
        return render(request, "locations/add_study_space.html", context=context)


def study_space_view(request, study_space_id):
    study_space = get_object_or_404(StudySpaces, pk=study_space_id)
    context = {
        "study_space": study_space,
        "lat": study_space.lat,
        "lng": study_space.lng,
        "api_key": settings.GOOGLE_API_KEY,
        "author": study_space.author,
    }
    if not study_space.active or (
        not study_space.is_verified and not request.user.is_staff
    ):
        return redirect("locations:index")
    return render(request, "locations/study_space.html", context=context)


def activity_view(request, activity_id):
    activity = get_object_or_404(Activities, pk=activity_id)
    context = {
        "activity": activity,
        "lat": activity.lat,
        "lng": activity.lng,
        "api_key": settings.GOOGLE_API_KEY,
        "author": activity.author,
    }
    if not activity.active or (not activity.is_verified and not request.user.is_staff):
        return redirect("locations:index")
    return render(request, "locations/activity.html", context=context)


def delete_activity(request, activity_id):
    activity = get_object_or_404(Activities, pk=activity_id)
    if not (request.user.is_staff or request.user == activity.author):
        return redirect("locations:index")

    activity.active = False
    activity.save()

    return redirect("locations:index")


def modify_activity(request, activity_id):
    activity = get_object_or_404(Activities, pk=activity_id)
    if not request.user.is_staff and not request.user == activity.author:
        return redirect("locations:activity_view", activity_id=activity.id)

    if request.method == "POST":
        new_name = request.POST.get("a_name")
        new_loc = request.POST.get("l_name")
        new_time = request.POST.get("activity_time")
        new_lat = request.POST.get("lat")
        new_lng = request.POST.get("lng")
        new_reservation = request.POST.getlist("reservation")
        new_loc_info = request.POST.get("location_details")
        new_incentives = request.POST.get("incentives")
        new_max_occ = request.POST.get("maximum_occupancy")

        activity.name = new_name if len(new_name.strip()) != 0 else activity.name
        activity.location = new_loc if len(new_loc.strip()) != 0 else activity.location
        activity.date_time = new_time if new_time else activity.date_time
        activity.lat = new_lat
        activity.lng = new_lng
        activity.reservation = True if len(new_reservation) > 0 else False
        activity.location_details = new_loc_info
        activity.incentives = new_incentives
        activity.maximum_occupancy = new_max_occ

        if not request.user.is_staff:
            activity.is_verified = False

        activity.save()
        return redirect("locations:activity_view", activity_id=activity.id)
    else:
        context = {
            "api_key": settings.GOOGLE_API_KEY,
            "activity": activity,
            "lat": activity.lat,
            "lng": activity.lng,
            "date_time": activity.date_time.strftime("%Y-%m-%dT%H:%M"),
        }
        return render(request, "locations/edit_activity_admin.html", context=context)


def delete_studyspace(request, study_space_id):
    study_space = get_object_or_404(StudySpaces, pk=study_space_id)
    if not (request.user.is_staff or request.user == study_space.author):
        return redirect("locations:index")

    study_space.active = False
    study_space.save()

    return redirect("locations:index")


def modify_studyspace(request, study_space_id):
    study_space = get_object_or_404(StudySpaces, pk=study_space_id)
    if not request.user.is_staff and not request.user == study_space.author:
        return redirect("locations:study_space_view", study_space_id=study_space_id)

    if request.method == "POST":
        new_name = request.POST.get("a_name")
        new_loc = request.POST.get("l_name")
        new_noise = int(request.POST.get("noise_level"))
        new_start_hours = request.POST.get("start_hours")
        new_end_hours = request.POST.get("end_hours")
        new_lat = request.POST.get("lat")
        new_lng = request.POST.get("lng")
        new_reservation = request.POST.getlist("reservation")
        new_loc_info = request.POST.get("location_details")
        new_amenities = request.POST.get("amenities")
        new_max_occ = request.POST.get("maximum_occupancy")

        # correct noise level if out of bounds
        if 5 < new_noise or new_noise < 1:
            new_noise = min(max(new_noise, 1), 5)

        study_space.name = new_name if len(new_name.strip()) > 0 else study_space.name
        study_space.location = (
            new_loc if len(new_loc.strip()) > 0 else study_space.location
        )

        study_space.noise_level = new_noise
        study_space.start_hours = (
            new_start_hours if new_start_hours else study_space.start_hours
        )
        study_space.end_hours = (
            new_end_hours if new_end_hours else study_space.end_hours
        )
        study_space.lat = new_lat
        study_space.lng = new_lng
        study_space.location_details = new_loc_info
        study_space.reservation = True if len(new_reservation) > 0 else False
        study_space.amenities = new_amenities
        study_space.maximum_occupancy = new_max_occ

        if not request.user.is_staff:
            study_space.is_verified = False

        study_space.save()

        return redirect("locations:study_space_view", study_space_id=study_space.id)
    else:
        context = {
            "api_key": settings.GOOGLE_API_KEY,
            "study_space": study_space,
            "lat": study_space.lat,
            "lng": study_space.lng,
            "start_hours": study_space.start_hours.strftime("%H:%M"),
            "end_hours": study_space.end_hours.strftime("%H:%M"),
        }
        return render(request, "locations/edit_studyspace_admin.html", context=context)


def error_404(request, exception=None, template_name="locations/error.html"):
    response = render(request, template_name, status=404, context={"status": 404})
    return response


def error_500(request, exception=None, template_name="locations/error.html"):
    response = render(request, template_name, status=500, context={"status": 500})
    return response


def error_403(request, exception=None, template_name="locations/error.html"):
    response = render(request, template_name, status=403, context={"status": 403})
    return response
