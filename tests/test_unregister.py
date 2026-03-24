"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint using the AAA pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering a student from an activity."""

    def test_unregister_successfully_removes_participant(self, client, reset_activities):
        """
        ARRANGE: Identify a participant already in an activity
        ACT: Send DELETE request to unregister that participant
        ASSERT: Participant is removed and response is successful
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity_name}"

        # Verify participant was actually removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities[activity_name]["participants"]

    def test_unregister_fails_for_nonexistent_participant(self, client, reset_activities):
        """
        ARRANGE: Prepare an email that's not registered for the activity
        ACT: Attempt to unregister that email
        ASSERT: Request fails with 404 status
        """
        # Arrange
        activity_name = "Chess Club"
        non_registered_email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": non_registered_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found in this activity"

    def test_unregister_fails_for_nonexistent_activity(self, client, reset_activities):
        """
        ARRANGE: Prepare a fake activity name
        ACT: Send DELETE request for non-existent activity
        ASSERT: Request fails with 404 status
        """
        # Arrange
        fake_activity = "Underwater Basket Weaving"
        test_email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{fake_activity}/unregister",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_does_not_affect_other_participants(self, client, reset_activities):
        """
        ARRANGE: Activity has multiple participants
        ACT: Unregister one participant
        ASSERT: Other participants remain registered
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        other_email = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200

        # Verify only the target email was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert other_email in activities[activity_name]["participants"]

    def test_unregister_updates_participant_count(self, client, reset_activities):
        """
        ARRANGE: Get initial participant count
        ACT: Unregister a participant
        ASSERT: Participant count decreases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert unregister_response.status_code == 200

        # Get updated count
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])

        assert updated_count == initial_count - 1

    def test_unregister_returns_correct_response_format(self, client, reset_activities):
        """
        ARRANGE: Prepare unregister parameters
        ACT: Send DELETE request
        ASSERT: Response has correct JSON structure
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        json_response = response.json()

        # Assert
        assert "message" in json_response
        assert isinstance(json_response["message"], str)
        assert activity_name in json_response["message"]
        assert email in json_response["message"]
