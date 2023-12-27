from django.test import TestCase
from django.contrib.auth.models import User
from .helper_functions import create_Activities, create_StudySpace
from ..models import StudySpaces, Activities
from django.utils import timezone
from django.urls import reverse


class TestModel(TestCase):
    def test_create_studyspace(self):
        """
        tst the StudySpaces model to ensure proper storage of data
        """
        studyspace = create_StudySpace(
            location="Rotunda", name="Rotunda Library", is_verified=True
        )
        studyspace2 = create_StudySpace(
            location="MacDonalds", name="Not Rotunda", is_verified=False
        )

        self.assertEquals(studyspace.location, "Rotunda")
        self.assertEquals(studyspace.name, "Rotunda Library")
        self.assertTrue(studyspace.is_verified)

        self.assertEquals(studyspace2.location, "MacDonalds")
        self.assertEquals(studyspace2.name, "Not Rotunda")
        self.assertTrue(not studyspace2.is_verified)

    def test_create_activities(self):
        """
        test the Activities model to ensure proper storage of data
        """
        activity = create_Activities(
            location="AFC", name="Workout Session", is_verified=True, days=30
        )
        activity2 = create_Activities(
            location="Slaughter",
            name="Other Workout Session",
            is_verified=False,
            days=30,
        )

        self.assertEquals(activity.location, "AFC")
        self.assertEquals(activity.name, "Workout Session")
        self.assertTrue(activity.is_verified)
        self.assertGreaterEqual(activity.date_time, timezone.now())

        self.assertEquals(activity2.location, "Slaughter")
        self.assertEquals(activity2.name, "Other Workout Session")
        self.assertTrue(not activity2.is_verified)
        self.assertGreaterEqual(activity2.date_time, timezone.now())

    def test_activity_upcoming(self):
        """
        Test the is_upcoming method to ensure that only activities that are scheduled
        for the future return true
        """
        upcoming_activity = create_Activities(
            location="Test", name="Test", is_verified=True, days=6
        )
        past_activity = create_Activities(
            location="Test 2", name="Test 2", is_verified=True, days=-1
        )

        self.assertEqual(upcoming_activity.is_upcoming(), True)
        self.assertEqual(past_activity.is_upcoming(), False)

    def test_activity_is_coming_soon(self):
        """
        Test the is_coming_soon method to ensure that only
        activities that are scheduled within the next week
        are displayed
        """
        coming_soon_activity = create_Activities(
            location="Test", name="Test", is_verified=True, days=6
        )
        past_activity = create_Activities(
            location="Test", name="Test", is_verified=True, days=-1
        )

        self.assertEqual(coming_soon_activity.is_coming_soon(), True)
        self.assertEqual(past_activity.is_coming_soon(), False)

    def test_study_space_available_now(self):
        """
        Test the is_available_now method to ensure
        that only study spaces that are currently available
        are displayed
        """
        now_space = create_StudySpace(location="Test", name="Test", is_verified=True)
        week_ago_space = create_StudySpace(
            location="Test 2", name="Test 2", is_verified=True, days=-8
        )
        week_future_space = create_StudySpace(
            location="Test 3", name="Test 3", is_verified=True, days=8
        )

        self.assertEqual(now_space.is_available_now(), True)
        self.assertEqual(week_ago_space.is_available_now(), True)
        self.assertEqual(week_future_space.is_available_now(), False)

    def test_is_available_soon(self):
        """
        Test the is_available_soon method to ensure it only returns
        true if the study space is available soon.
        """
        now_space = create_StudySpace(location="Test", name="Test", is_verified=True)
        week_ago_space = create_StudySpace(
            location="Test 2", name="Test 2", is_verified=True, days=-8
        )
        week_future_space = create_StudySpace(
            location="Test 3", name="Test 3", is_verified=True, days=6
        )

        self.assertEqual(now_space.is_available_soon(), False)
        self.assertEqual(week_ago_space.is_available_soon(), False)
        self.assertEqual(week_future_space.is_available_soon(), True)

    def test_study_space_noise_level(self):
        """
        Test noise level to make sure it is properly stored
        """
        level_1_space = create_StudySpace(
            location="Test", name="Test", is_verified=True, noise_level=1
        )
        level_5_space = create_StudySpace(
            location="Test", name="Test", is_verified=True, noise_level=5
        )
        self.assertEqual(level_1_space.noise_level, 1)
        self.assertEqual(level_5_space.noise_level, 5)
