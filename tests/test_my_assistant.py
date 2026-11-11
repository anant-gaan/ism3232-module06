# tests/test_my_assistant.py
# Author: Anant Gaan

from fake_model import FakeModel
from mock_model import MockModel
from my_assistant import StudyRoomAssistant
from my_reservation_queue import ReservationQueue
from my_tool import RoomLookup
from my_toolbox import StudyRoomToolbox


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


def test_cancellation_request_goes_to_front_desk():
    assistant = make_assistant()
    reply = assistant.respond("Can you cancel my reservation?")
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


def test_model_chooses_room_lookup():
    rooms = RoomLookup({"library": "Room 101 and Room 103"})
    queue = ReservationQueue()
    tools = StudyRoomToolbox(rooms, queue)
    model = FakeModel(
        [
            {
                "tool": "check_available_rooms",
                "arguments": {"building": "library"},
            },
            {"text": "Available rooms in library: Room 101 and Room 103."},
        ]
    )
    assistant = StudyRoomAssistant("Casey", "Be helpful.", rooms, model, tools)

    reply = assistant.respond("Which rooms are available in the library?")

    assert "Room 101" in reply
    assert model.calls == 2
    assert assistant.history[1]["role"] == "tool"


def test_reservation_rejects_invented_student():
    rooms = RoomLookup({"library": "Room 101 and Room 103"})
    queue = ReservationQueue()
    tools = StudyRoomToolbox(rooms, queue)
    model = FakeModel(
        [
            {
                "tool": "request_reservation",
                "arguments": {
                    "building": "library",
                    "room": "Room 101",
                    "student": "Alex",
                },
            },
            {"text": "Please provide your name."},
        ]
    )
    assistant = StudyRoomAssistant("Casey", "Be helpful.", rooms, model, tools)

    assistant.respond("Please reserve Room 101 in the library.")

    assert queue.waiting() == []
    assert "not given that name" in assistant.history[1]["content"]


def test_valid_reservation_waits_for_approval():
    rooms = RoomLookup({"library": "Room 101 and Room 103"})
    queue = ReservationQueue()
    tools = StudyRoomToolbox(rooms, queue)
    model = FakeModel(
        [
            {
                "tool": "request_reservation",
                "arguments": {
                    "building": "library",
                    "room": "Room 101",
                    "student": "Alex",
                },
            },
            {"text": "Your request is waiting for front desk approval."},
        ]
    )
    assistant = StudyRoomAssistant("Casey", "Be helpful.", rooms, model, tools)

    assistant.respond("I'm Alex. Reserve Room 101 in the library.")

    assert len(queue.waiting()) == 1
    assert queue.reservations == []
    assert model.calls == 2


def test_front_desk_approves_reservation_once():
    queue = ReservationQueue()
    queue.request_reservation("library", "Room 101", "Alex")

    assert len(queue.waiting()) == 1
    assert queue.reservations == []

    queue.approve(1)

    assert queue.waiting() == []
    assert len(queue.reservations) == 1

    queue.approve(1)

    assert len(queue.reservations) == 1


def test_front_desk_rejects_reservation():
    queue = ReservationQueue()
    queue.request_reservation("library", "Room 101", "Alex")

    assert len(queue.waiting()) == 1

    queue.reject(1)

    assert queue.waiting() == []
    assert queue.reservations == []

    queue.approve(1)

    assert queue.reservations == []


def test_cancellation_handoff_skips_model():
    rooms = RoomLookup({"library": "Room 101 and Room 103"})
    queue = ReservationQueue()
    tools = StudyRoomToolbox(rooms, queue)
    model = FakeModel([{"text": "I can cancel that for you."}])
    assistant = StudyRoomAssistant("Casey", "Be helpful.", rooms, model, tools)

    reply = assistant.respond("Please cancel my room reservation.")

    assert "front desk" in reply
    assert model.calls == 0
    assert queue.waiting() == []
