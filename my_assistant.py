# my_assistant.py
# Author: Anant Gaan

HANDOFF_WORDS = ["cancel", "change"]
MAX_TOOL_ROUNDS = 3


class StudyRoomAssistant:
    """A mock assistant that helps students check study room availability."""

    def __init__(self, name, instructions, room_lookup, model, tools=None):
        """Set up the assistant with its name, instructions, tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.room_lookup = room_lookup
        self.model = model
        self.tools = tools
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, and save both."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Hand off certain requests before asking the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't handle cancellations or changes. I'm passing you to the front desk."
        if self.tools is None and ("available" in text or "rooms" in text):
            return self.rooms_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """Ask the model, run requested tools, and stop after a limit."""
        if self.tools is None:
            reply = self.model.reply(self.instructions, self.history)
            if reply is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."
            return reply

        rounds = 0
        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)

            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."

            if "text" in decision:
                return decision["text"]

            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)

            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            rounds += 1

        return "Sorry, I couldn't finish that. I'm passing you to the front desk."

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
