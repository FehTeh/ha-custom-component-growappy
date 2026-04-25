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
    def full_name(self):
        return self._data["full_name"]

    @property
    def status(self):
        return self._data["status"]

    @property
    def school_class(self):
        try:
            return self._data["school_class"]["name"]
        except (KeyError, TypeError):
            return None
    
    @property
    def school_year(self):
        try:
            return self._data["school_class"]["school_year"]["name"]
        except (KeyError, TypeError):
            return None

    @property
    def school_name(self):
        try:
            return self._data["school_class"]["school_year"]["school"]["name"]
        except (KeyError, TypeError):
            return None
