# my_main.py
# Author: Anant Gaan

from my_assistant import StudyRoomAssistant
from my_reservation_queue import ReservationQueue
from my_tool import RoomLookup
from my_toolbox import StudyRoomToolbox
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Casey, a study room assistant for Campus Study Hub.
Answer in one short sentence.
The study hub is open from 8 am to 10 pm every day.
Students must bring their student ID to use a study room.
You can check available rooms in the library, student center, and business hall.
Use check_available_rooms when a student asks about room availability.
Use request_reservation when a student wants to reserve a room.
Before requesting a reservation, get the building, room, and student's name.
Only use information the student actually provided.
Reservation requests must be approved by the front desk.
Never tell a student that a room is reserved before approval.
Cancellations and reservation changes must go to the front desk.
If you do not know something, suggest asking the front desk."""

ROOMS = {
    "library": "Room 101 and Room 103",
    "student center": "Room 204",
    "business hall": "none",
}

room_lookup = RoomLookup(ROOMS)
reservation_queue = ReservationQueue()
tools = StudyRoomToolbox(room_lookup, reservation_queue)
model = OllamaModel(MODEL_NAME)
assistant = StudyRoomAssistant("Casey", INSTRUCTIONS, room_lookup, model, tools)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
print("Reservation requests waiting for front desk approval:")
for request in reservation_queue.waiting():
    print(request)
    answer = input("Approve this request? (yes/no): ")
    if answer == "yes":
        print(reservation_queue.approve(request["number"]))
    else:
        print(reservation_queue.reject(request["number"]))
