# my_reservation_queue.py
# Author: Anant Gaan


class ReservationQueue:
    """Study room requests waiting for front desk approval."""

    def __init__(self):
        """Start with no requests and no approved reservations."""
        self.requests = []
        self.reservations = []

    def request_reservation(self, building, room, student):
        """Ask the front desk to reserve a study room.

        Args:
            building: The building name, like library.
            room: The room number, like Room 101.
            student: The student's name.
        """
        number = len(self.requests) + 1
        request = {
            "number": number,
            "building": building,
            "room": room,
            "student": student,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to the front desk. Nothing is reserved yet."

    def waiting(self):
        """Return requests still waiting for approval."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Find a request by its number."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve a waiting request and record the reservation once."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        request["status"] = "approved"
        self.reservations.append(
            {
                "building": request["building"],
                "room": request["room"],
                "student": request["student"],
            }
        )
        return f"Request {number} approved."

    def reject(self, number):
        """Reject a waiting request without reserving a room."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        request["status"] = "rejected"
        return f"Request {number} rejected."
