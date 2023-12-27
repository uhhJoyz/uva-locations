from django.test import TestCase
from django.contrib.auth.models import User
from .helper_functions import create_Activities, create_StudySpace
from ..models import StudySpaces, Activities
from django.utils import timezone
import datetime
from django.urls import reverse


class TestAdminHomepage(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_admin", email="test@test.com", is_staff=True
        )
        self.client.force_login(self.user)

    def test_no_activities(self):
        """
        If no activites are in the database, an appropriate message is displayed.
        """
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no study spaces to display.")

    def test_no_study_spaces(self):
        """
        If no study spaces are in the database, an appropriate message is displayed.
        """
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no activities to display.")

    def test_activity_added_verified(self):
        """
        If an activity is added, it can be viewed properly
        """
        a = Activities.objects.create(
            date_time=timezone.now() + datetime.timedelta(days=20),
            location="Testing",
            name="Testing",
            is_verified=True,
        )
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name: Testing")
        self.assertContains(response, "Location: Testing")
        self.assertContains(response, "There are currently no study spaces to display.")
        self.assertQuerySetEqual(response.context["activities"], [a])

    def study_space_added_verified(self):
        """
        If a study space is added, it can be viewed properly
        """
        ss = StudySpaces.objects.create(
            location="Testing", name="Testing", is_verified=True
        )
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        # test response
        self.assertEqual(response.status_code, 200)
        # test webpage is displaying properly
        self.assertContains(response, "There are currently no activities to display.")
        self.assertContains(response, "Name: Testing")
        self.assertContains(response, "Location: Testing")
        # test queryset of page
        self.assertQuerySetEqual(response.context["study_spaces"], [ss])

    def test_study_space_added_unverified(self):
        """
        If a study space is added, it can be viewed properly
        """
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        StudySpaces.objects.create(
            location="Testing", name="Testing", is_verified=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no activities to display.")
        self.assertContains(response, "There are currently no study spaces to display.")
        # test queryset of page
        self.assertQuerySetEqual(response.context["study_spaces"], [])

    def test_activity_added_unverified(self):
        """
        If a study space is added, it can be viewed properly
        """
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        Activities.objects.create(location="Testing", name="Testing", is_verified=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no activities to display.")
        self.assertContains(response, "There are currently no study spaces to display.")
        self.assertQuerySetEqual(response.context["activities"], [])
