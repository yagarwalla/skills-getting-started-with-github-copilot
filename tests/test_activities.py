"""
Tests for the GET /activities endpoint using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        ARRANGE: No additional setup needed - client is ready
        ACT: Send GET request to /activities
        ASSERT: Response status is 200 and contains all expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Robotics Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        ARRANGE: No additional setup needed
        ACT: Send GET request to /activities
        ASSERT: Response contains all required fields for each activity
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants"
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_details, dict)
            assert required_fields.issubset(activity_details.keys())
            assert isinstance(activity_details["participants"], list)
            assert isinstance(activity_details["max_participants"], int)

    def test_get_activities_includes_existing_participants(self, client, reset_activities):
        """
        ARRANGE: Activities have pre-loaded participants
        ACT: Send GET request to /activities
        ASSERT: Participants are included in the response
        """
        # Arrange
        # Activities already have participants from the app.py initialization

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) > 0
        assert "michael@mergington.edu" in chess_club["participants"]
