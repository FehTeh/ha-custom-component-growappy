"""Metric Class."""

class Metric:
    """Represents a Growappy diary metric."""

    def __init__(self, data):
        self._data = data
        
    @property
    def id(self):
        return self._data["metric_type"]

    @property
    def type(self):
        return self._data["metric_type_detail"]["type"]

    @property
    def state(self):
        return self._data["metric_state"]

    @property
    def start(self):
        return self._data["metric_start"]

