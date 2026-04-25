"""Base Entity for Growappy."""

from __future__ import annotations

from .api.growappy import GROWAPPY
from .api.student import Student

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class GrowappyDevice(Entity):
    """Common Growappy Device Information."""

    _attr_has_entity_name = True

    def __init__(self, api: GROWAPPY, student: Student) -> None:
        """Initialize device information."""
        self._api = api
        self._student = student
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={
                (
                    DOMAIN,
                    f"{student.id}",
                )
            },
            manufacturer=DOMAIN,
            name=student.full_name,
        )