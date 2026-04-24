"""Platform for binary sensor integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from logging import config
from typing import Any, Callable, Dict

import aiohttp
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.growappy import GROWAPPY
from .api.student import Student
from .const import DOMAIN, DEFAULT_ICON, ATTRIBUTION

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass: HomeAssistant, 
                            config_entry: ConfigEntry, 
                            async_add_entities: Callable):
    """Setup binary sensor platform."""
    session = async_get_clientsession(hass, True)
    api = GROWAPPY(session)

    config = config_entry.data

    # TODO check token refresh
    token = config["access_token"]

    students = await api.getStudents(token)
    sensors = [GrowappyStudentBinarySensor(student, api, config) for student in students]
    async_add_entities(sensors, update_before_add=True)


class GrowappyStudentBinarySensor(BinarySensorEntity):
    """Representation of a student as a Binary Sensor (Presence)."""

    def __init__(self, student: Student, api: GROWAPPY, config: Any):
        """Initialize the binary sensor."""
        super().__init__()
        self._student = student
        self._api = api
        self._config = config
        
        self._attr_name = f"Student {self._student.name}"
        self._attr_unique_id = f"{DOMAIN}-{self._student.id}-presence".lower()
        self._attr_device_class = BinarySensorDeviceClass.PRESENCE
        self._attr_icon = DEFAULT_ICON
        
        self._is_on = False
        self._available = True
        self._extra_attrs = {}

    @property
    def is_on(self) -> bool:
        """Returns True if the student is checked in."""
        return self._is_on

    @property
    def available(self) -> bool:
        return self._available

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Additional attributes to help with debugging or automation."""
        return {
            "student_name": self._student.name,
            "student_id": self._student.id,
            "attribution": ATTRIBUTION,
            **self._extra_attrs
        }

    async def async_update(self) -> None:
        """Fetches the diary data and sets the presence status."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # TODO check token refresh
            token = self._config["access_token"]
            
            metrics = await self._api.getDiary(token, self._student.id, today, today)
            
            if metrics and len(metrics) > 0:
                # Pegamos o último elemento do array como você pediu
                last_metric = metrics[-1]
                
                self._is_on = last_metric.state == 1
                self._extra_attrs["last_event"] = last_metric.state
                self._extra_attrs["last_update"] = last_metric.start
            else:
                self._is_on = False
            
            self._available = True

        except aiohttp.ClientError as err:
            self._available = False
            _LOGGER.error("Error updating Growappy Student %s: %s", self._student.name, err)