"""
Tests for the POST /activities/{activity_name}/signup endpoint using the AAA pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""

    def test_signup_successfully_adds_participant(self, client, reset_activities):
        """
        ARRANGE: Prepare a new email and activity name
        ACT: Send POST request to sign up for an activity
        ASSERT: Participant is added and response is successful
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"

        # Verify participant was actually added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities[activity_name]["participants"]

    def test_signup_prevents_duplicate_registration(self, client, reset_activities):
        """
        ARRANGE: Verify an email that's already registered
        ACT: Attempt to sign up that email again
        ASSERT: Request fails with 400 status and appropriate message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Already signed up for this activity"

    def test_signup_fails_for_nonexistent_activity(self, client, reset_activities):
        """
        ARRANGE: Prepare a fake activity name
        ACT: Send POST request for non-existent activity
        ASSERT: Request fails with 404 status
        """
        # Arrange
        fake_activity = "Underwater Basket Weaving"
        test_email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_allows_same_email_for_different_activities(self, client, reset_activities):
        """
        ARRANGE: Prepare one email and two different activities
        ACT: Sign up the same email for two different activities
        ASSERT: Both signups succeed
        """
        # Arrange
        email = "multitasker@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act - Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )

        # Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_returns_correct_response_format(self, client, reset_activities):
        """
        ARRANGE: Prepare signup parameters
        ACT: Send POST request
        ASSERT: Response has correct JSON structure
        """
        # Arrange
        activity_name = "Gym Class"
        email = "athlete@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        json_response = response.json()

        # Assert
        assert "message" in json_response
        assert isinstance(json_response["message"], str)
        assert activity_name in json_response["message"]
        assert email in json_response["message"]
