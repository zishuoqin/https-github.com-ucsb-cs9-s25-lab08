# Event.py

def format(time):
    """Convert (start, end) integers like (1530, 1645) to '15:30 - 16:45'."""
    return f"{time[0]//100:0>2}:{time[0]%100:0>2} - {time[1]//100:0>2}:{time[1]%100:0>2}"


class Event:
    """Represents a lecture or section meeting time and place."""

    def __init__(self, day, time, location):
        # day: a string like 'MW', 'TR', 'F'
        # time: (start, end) in 24-hour int format, e.g. (1530, 1645)
        # location: stored in uppercase
        self.day = day
        self.time = time
        self.location = location.upper()

    def __eq__(self, rhs):
        # Two events identical if day, time, and location all match
        if not isinstance(rhs, Event):
            return False
        return (
            self.day == rhs.day
            and self.time == rhs.time
            and self.location == rhs.location
        )

    def __str__(self):
        # Example: 'TR 15:30 - 16:45, TD-W 1701'
        return f"{self.day} {format(self.time)}, {self.location}"
