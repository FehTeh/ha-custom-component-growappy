"""Token Class."""

class Token:
    """Represents a Growappy token."""

    def __init__(self, data):
        self._data = data

    @property
    def refresh(self):
        return self._data["refresh"]

    @property
    def access(self):
        return self._data["access"]