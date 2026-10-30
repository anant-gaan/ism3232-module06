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
