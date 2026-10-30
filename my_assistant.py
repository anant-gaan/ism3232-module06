# my_assistant.py
# Author: Anant Gaan

HANDOFF_WORDS = ["reserve", "cancel", "change"]


class StudyRoomAssistant:
    """A mock assistant that helps students check study room availability."""

    def __init__(self, name, instructions, room_lookup):
        """Set up the assistant with its name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.room_lookup = room_lookup
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, and save both."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply using simple keyword rules."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't make reservations. I'm passing you to the front desk."
        if "available" in text or "rooms" in text:
            return self.rooms_reply(user_message)
        if "hello" in text:
            return (
                f"Hello! I'm {self.name}. I can check which study rooms are available."
            )
        return (
            "I'm not sure how to help with that. I can check study room availability."
        )

    def needs_human(self, text):
        """Return True if the student wants to change a room reservation."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def rooms_reply(self, user_message):
        """Use the room lookup tool to answer an availability question."""
        building = self.room_lookup.find_building(user_message)
        if building is None:
            return (
                "Which building? I can check library, student center, or business hall."
            )
        rooms = self.room_lookup.rooms_for(building)
        return f"Available rooms in {building}: {rooms}."
