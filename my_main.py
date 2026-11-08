# my_main.py
# Author: Anant Gaan

from my_assistant import StudyRoomAssistant
from my_tool import RoomLookup
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Casey, a study room assistant for Campus Study Hub.
Answer in one short sentence.
The study hub is open from 8 am to 10 pm every day.
Students must bring their student ID to use a study room.
Only state facts that appear in these instructions.
If you do not know, say you do not know and suggest asking the front desk."""

ROOMS = {
    "library": "Room 101 and Room 103",
    "student center": "Room 204",
    "business hall": "none",
}

room_lookup = RoomLookup(ROOMS)
model = OllamaModel(MODEL_NAME)
assistant = StudyRoomAssistant("Casey", INSTRUCTIONS, room_lookup, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
