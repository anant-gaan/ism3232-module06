# tests/test_my_assistant.py
# Author: Anant Gaan

from mock_model import MockModel
from my_assistant import StudyRoomAssistant
from my_tool import RoomLookup


class SilentModel:
    """A model that has no answer."""

    def reply(self, instructions, history):
        return None


def make_assistant():
    """Build a fresh study room assistant with its own tool for each test."""
    rooms = RoomLookup(
        {
            "library": "Room 101 and Room 103",
            "student center": "Room 204",
            "business hall": "none",
        }
    )
    return StudyRoomAssistant("Casey", "Be helpful.", rooms, MockModel())


def test_known_building_uses_room_tool():
    assistant = make_assistant()
    reply = assistant.respond("Which rooms are available in the library?")
    assert reply == "Available rooms in library: Room 101 and Room 103."


def test_unknown_building_asks_for_one():
    assistant = make_assistant()
    reply = assistant.respond("Are there any rooms available in the gym?")
    assert "Which building?" in reply


def test_reservation_request_goes_to_front_desk():
    assistant = make_assistant()
    reply = assistant.respond("Can you reserve Room 101 for me?")
    assert "front desk" in reply


def test_unknown_question_gets_safe_reply():
    rooms = RoomLookup({"library": "Room 101 and Room 103"})
    assistant = StudyRoomAssistant("Casey", "Be helpful.", rooms, SilentModel())
    reply = assistant.respond("Do you sell coffee?")
    assert "try again" in reply


def test_conversation_records_both_roles():
    assistant = make_assistant()
    assistant.respond("hello")
    assistant.respond("Which rooms are available in the library?")
    assert len(assistant.history) == 4
    assert assistant.history[0]["role"] == "user"
    assert assistant.history[1]["role"] == "assistant"


def test_other_messages_go_to_the_model():
    assistant = make_assistant()
    assert assistant.respond("hello") == "Hello! How can I help you today?"
