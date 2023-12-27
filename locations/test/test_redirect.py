from django.test import TestCase
from django.contrib.auth.models import User
from .helper_functions import create_Activities, create_StudySpace
from ..models import StudySpaces, Activities
from django.utils import timezone
from django.urls import reverse


class TestUserRedirects(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@testing.com",
            is_staff=False,
        )
        self.client.force_login(self.user)

    def test_unapproved_activity_redirect(self):
        """
        Test the user redirect from an unapproved activity
        """
        activity = create_Activities(location="Test", name="Test", is_verified=False)
        response = self.client.get(
            reverse("locations:activity_view", args=[activity.id]), secure=True
        )
        self.assertEqual(response.status_code, 302)

    def test_unapproved_study_space_redirect(self):
        """
        Test the user redirect from an unapproved study space to the homepage
        """
        study_space = create_StudySpace(location="Test", name="Test", is_verified=False)
        response = self.client.get(
            reverse("locations:study_space_view", args=[study_space.id]), secure=True
        )
        self.assertEqual(response.status_code, 302)

    def test_user_redirect_from_admin(self):
        response = self.client.get(reverse("locations:admin_home"), secure=True)
        self.assertEqual(response.status_code, 302)

    def test_user_redirect_from_deleted_study_space(self):
        """
        Test the redirect from a deleted study space back to the homepage
        """
        study_space = create_StudySpace(
            location="Test", name="Test", is_verified=True, active=False
        )
        response = self.client.get(
            reverse("locations:study_space_view", args=[study_space.id]), secure=True
        )
        self.assertEqual(response.status_code, 302)

    def test_user_redirect_from_deleted_activity(self):
        """
        Test the redirect from a deleted activity back to the homepage
        """
        activity = create_Activities(
            location="Test", name="Test", is_verified=True, active=False
        )
        response = self.client.get(
            reverse("locations:activity_view", args=[activity.id]), secure=True
        )
        self.assertEqual(response.status_code, 302)


class TestAdminRedirects(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_admin", email="test@test.com", is_staff=True
        )
        self.client.force_login(self.user)

    def test_admin_redirect_from_index(self):
        """
        Test that admins are automatically redirected to the admin homepage
        """
        response = self.client.get(reverse("locations:index"), secure=True)
        self.assertEqual(response.status_code, 302)

    def test_admin_no_redirect_from_unverified_study_space(self):
        """
        Test to make sure that admins can view unverified study spaces
        """
        study_space = create_StudySpace(location="Test", name="Test", is_verified=False)
        response = self.client.get(
            reverse("locations:study_space_view", args=[study_space.id]), secure=True
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_no_redirect_from_unverified_activity(self):
        """
        Test to make sure that admins can view unverified activities
        """
        activity = create_Activities(location="Test", name="Test", is_verified=False)
        response = self.client.get(
            reverse("locations:activity_view", args=[activity.id]), secure=True
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_redirect_from_deleted_study_space(self):
        """
        Test the admin redirect from a deleted study space back to the homepage
        """
        study_space = create_StudySpace(
            location="Test", name="Test", is_verified=True, active=False
        )
        response = self.client.get(
            reverse("locations:study_space_view", args=[study_space.id]), secure=True
        )
        self.assertEqual(response.status_code, 302)

    def test_admin_redirect_from_deleted_activity(self):
        """
        Test the admin redirect from a deleted activity back to the homepage
        """
        activity = create_Activities(
            location="Test", name="Test", is_verified=True, active=False
        )
        response = self.client.get(
            reverse("locations:activity_view", args=[activity.id]), secure=True
        )
        self.assertEqual(response.status_code, 302)
