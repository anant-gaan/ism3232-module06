# my_main.py
# Author: Anant Gaan

from my_assistant import StudyRoomAssistant
from my_tool import RoomLookup

ROOMS = {
    "library": "Room 101 and Room 103",
    "student center": "Room 204",
    "business hall": "none",
}

room_lookup = RoomLookup(ROOMS)
assistant = StudyRoomAssistant(
    "Casey",
    "You help students at Campus Study Hub check available study rooms.",
    room_lookup,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
