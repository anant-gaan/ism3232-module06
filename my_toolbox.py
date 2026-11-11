# my_toolbox.py
# Author: Anant Gaan


class StudyRoomToolbox:
    """Check every tool request before allowing Casey to run it."""

    def __init__(self, room_lookup, reservation_queue):
        """Store Casey's allowed tools."""
        self.room_lookup = room_lookup
        self.reservation_queue = reservation_queue

    def tool_list(self):
        """Return the tools Casey may ask to use."""
        return [
            self.room_lookup.check_available_rooms,
            self.reservation_queue.request_reservation,
        ]

    def run(self, name, arguments, history):
        """Check a tool request before running it."""
        if name == "check_available_rooms":
            building = self.clean(arguments, "building")
            if building == "":
                return "The building is missing. Ask the student for it."
            if not self.customer_said(history, building):
                return "The student has not given that building. Ask them for it."
            return self.room_lookup.check_available_rooms(building)

        if name == "request_reservation":
            building = self.clean(arguments, "building")
            room = self.clean(arguments, "room")
            student = self.clean(arguments, "student")

            if building == "" or room == "" or student == "":
                return "The building, room, and student name are all needed."

            if not self.customer_said(history, building):
                return "The student has not given that building. Ask them for it."
            if not self.customer_said(history, room):
                return "The student has not given that room. Ask them for it."
            if not self.customer_said(history, student):
                return "The student has not given that name. Ask them for it."
            if not self.room_lookup.room_exists(building, room):
                return "That room is not available in that building."

            return self.reservation_queue.request_reservation(building, room, student)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return an argument as text without extra spaces."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Check whether the student actually supplied the text."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
