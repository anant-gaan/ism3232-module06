# my_tool.py
# Author: Anant Gaan


class RoomLookup:
    """A tool that knows which study rooms are available in each building."""

    def __init__(self, rooms):
        """Store the available rooms for each building."""
        self.rooms = rooms

    def find_building(self, text):
        """Return the first known building mentioned in text, or None."""
        for building in self.rooms:
            if building in text.lower():
                return building
        return None

    def rooms_for(self, building):
        """Return the available rooms for one building, or None if unknown."""
        if building in self.rooms:
            return self.rooms[building]
        return None

    def room_exists(self, building, room):
        """Return True if the room is listed in the building."""
        found = self.find_building(building)
        if found is None:
            return False

        rooms = self.rooms_for(found)
        return room.lower() in rooms.lower()

    def check_available_rooms(self, building):
        """Look up available study rooms in one building.

        Args:
            building: The building name, like library.
        """
        found = self.find_building(building)
        if found is None:
            return "That building was not found. I can check library, student center, or business hall."
        return f"Available rooms in {found}: {self.rooms_for(found)}."
