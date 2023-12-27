from django.test import TestCase
from django.contrib.auth.models import User
from .helper_functions import create_Activities, create_StudySpace
from ..models import StudySpaces, Activities
from django.utils import timezone
from django.urls import reverse


class TestUserHomepage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@testing.com",
            is_staff=False,
        )
        self.client.force_login(self.user)

    # test past activity -> shouldn't be there
    # test future activity -> should be there
    def test_past_activity(self):
        activity = create_Activities(
            location="AFC", name="Workout Session", is_verified=True, days=-30
        )
        response = self.client.get(reverse("locations:index"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["activities"], [])

    def test_future_activity(self):
        activity = create_Activities(
            location="AFC", name="Workout Session", is_verified=True, days=30
        )
        response = self.client.get(reverse("locations:index"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["activities"], [activity])

    def test_study_space_view_page(self):
        study_space = create_StudySpace(location="Test", name="Test", is_verified=True)
        response = self.client.get(
            reverse("locations:study_space_view", args=[study_space.id]), secure=True
        )
        self.assertContains(response, "Test")
        self.assertEqual(response.context["study_space"], study_space)

    def test_activity_view_page(self):
        activity = create_Activities(location="Test", name="Test", is_verified=True)
        response = self.client.get(
            reverse("locations:activity_view", args=[activity.id]), secure=True
        )
        self.assertContains(response, "Test")
        self.assertEqual(response.context["activity"], activity)

    def test_user_add_study_space_intended_use(self):
        """
        Test the intended use case for a form submission on the add study space page
        """
        post_context = {
            "a_name": "Stud",
            "l_name": "Loc",
            "noise_level": 1,
            "lat": 0.1,
            "lng": 0.2,
            "reservation": ["some item"],
            "location_details": "Details",
            "amenities": "Water fountain",
        }
        response = self.client.post(
            reverse("locations:add_study_space"), post_context, secure=True
        )
        study_space = StudySpaces.objects.filter(name="Stud")[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(study_space.reservation, True)
        self.assertEqual(study_space.noise_level, 1)
        self.assertEqual(study_space.location, "Loc")
        self.assertEqual(study_space.lat, 0.1)
        self.assertEqual(study_space.lng, 0.2)

    def test_user_noise_level_correction_below_one(self):
        """
        Test intended use case when the user enters
        a noise level that is out of bounds
        """
        post_context = {
            "a_name": "Stud",
            "l_name": "Loc",
            "noise_level": -4,
            "lat": 0.1,
            "lng": 0.2,
            "reservation": ["some item"],
            "location_details": "Details",
            "amenities": "Water fountain",
        }
        response = self.client.post(
            reverse("locations:add_study_space"), post_context, secure=True
        )
        study_space = StudySpaces.objects.filter(name="Stud")[0]
        self.assertEqual(study_space.noise_level, 1)

    def test_user_noise_level_correction_above_five(self):
        """
        Test intended use case when the user enters
        a noise level that is out of bounds
        """
        post_context = {
            "a_name": "Stud",
            "l_name": "Loc",
            "noise_level": 16,
            "lat": 0.1,
            "lng": 0.2,
            "reservation": ["some item"],
            "location_details": "Details",
            "amenities": "Water fountain",
        }
        response = self.client.post(
            reverse("locations:add_study_space"), post_context, secure=True
        )
        study_space = StudySpaces.objects.filter(name="Stud")[0]
        self.assertEqual(study_space.noise_level, 5)

    def test_user_add_study_space_no_checkbox(self):
        """
        Test the study space submission use case when the reservation box is not checked
        """
        post_context = {
            "a_name": "Stud",
            "l_name": "Loc",
            "noise_level": 1,
            "lat": 0.1,
            "lng": 0.2,
            "reservation": [],
            "location_details": "Details",
            "amenities": "Water fountain",
        }
        response = self.client.post(
            reverse("locations:add_study_space"), post_context, secure=True
        )
        study_space = StudySpaces.objects.filter(name="Stud")[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(study_space.reservation, False)

    def test_user_add_activity_intended_use(self):
        """
        Test the intended use case for a form submission on the add activity page
        """
        post_context = {
            "a_name": "Act",
            "l_name": "Loc",
            "activity_time": timezone.now(),
            "lat": 0.1,
            "lng": 0.2,
            "reservation": ["some item"],
            "location_details": "Details",
            "incentives": "Food",
        }
        response = self.client.post(
            reverse("locations:add_activity"), post_context, secure=True
        )
        study_space = Activities.objects.filter(name="Act")[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(study_space.name, "Act")
        self.assertEqual(study_space.reservation, True)
        self.assertEqual(study_space.location, "Loc")
        self.assertEqual(study_space.lat, 0.1)
        self.assertEqual(study_space.lng, 0.2)

    def test_user_add_activity_no_checkbox(self):
        """
        Test the activity submission use case when the reservation box is not checked
        """
        post_context = {
            "a_name": "Act",
            "l_name": "Loc",
            "activity_time": timezone.now(),
            "lat": 0.1,
            "lng": 0.2,
            "reservation": [],
            "location_details": "Details",
            "incentives": "Food",
        }
        response = self.client.post(
            reverse("locations:add_activity"), post_context, secure=True
        )
        study_space = Activities.objects.filter(name="Act")[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(study_space.reservation, False)
