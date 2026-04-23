"""Student Class."""

class Student:
    """Represents a Growappy student."""

    def __init__(self, data):
        self._data = data
        
    @property
    def id(self):
        return self._data["id"]

    @property
    def name(self):
        return self._data["name"]

    @property
    def status(self):
        return self._data["status"]

    @property
    def full_name(self):
        return self._data["full_name"]