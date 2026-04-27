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
from .api.exceptions import GrowappyUnauthorizedException
from .const import DOMAIN, ATTRIBUTION
from .entity import GrowappyDevice

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass: HomeAssistant, 
                            config_entry: ConfigEntry, 
                            async_add_entities: Callable):
    """Setup binary sensor platform."""
    session = async_get_clientsession(hass, True)
    api = GROWAPPY(session)
    config = config_entry.data

    try:
        students = await api.getStudents(config["access_token"])
    except GrowappyUnauthorizedException:
        try:
            token = await api.refreshToken(config["refresh_token"]);
        except Exception as err:
            _LOGGER.error("Failed to refresh token: %s", err)
            raise ConfigEntryAuthFailed("Failed to refresh token. Re-auth") from err

        new_config = {**config, "access_token": token.access, "refresh_token": token.refresh}
        hass.config_entries.async_update_entry(
            config_entry, data=new_config
        )
        config = new_config

        students = await api.getStudents(config["access_token"])

    sensors = [GrowappyStudentBinarySensor(student, api, config_entry) for student in students]
    async_add_entities(sensors, update_before_add=True)


class GrowappyStudentBinarySensor(BinarySensorEntity, GrowappyDevice):
    """Representation of a student as a Binary Sensor (Presence)."""

    def __init__(self, student: Student, api: GROWAPPY, config_entry: ConfigEntry):
        """Initialize the binary sensor."""
        GrowappyDevice.__init__(self, api, student)

        self._student = student
        self._api = api
        self._config_entry = config_entry

        self._attr_unique_id = f"{DOMAIN}_{self._student.id}_presence"
        self._attr_device_class = BinarySensorDeviceClass.PRESENCE
        self._attr_icon = "mdi:account-check"
        
        self._is_on = False
        self._available = True
        self._translation_key = "presence"
        self._extra_attrs = {}

    @property
    def is_on(self) -> bool:
        """Returns True if the student is checked in."""
        return self._is_on

    @property
    def available(self) -> bool:
        return self._available

    @property
    def translation_key(self) -> str:
        return self._translation_key

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
            config = self._config_entry.data

            try:
                metrics = await self._api.getDiary(config["access_token"], self._student.id, today, today)
            except GrowappyUnauthorizedException:
                try:
                    token = await self._api.refreshToken(config["refresh_token"]);
                except Exception as err:
                    _LOGGER.error("Failed to refresh token: %s", err)
                    raise ConfigEntryAuthFailed("Failed to refresh token. Re-auth") from err
                
                new_config = {**config, "access_token": token.access, "refresh_token": token.refresh}
                await self.hass.config_entries.async_update_entry(
                    self._config_entry, data=new_config
                )
                config = new_config   

                metrics = await self._api.getDiary(config["access_token"], self._student.id, today, today)

            if metrics and len(metrics) > 0:
                last_metric = metrics[-1]
                
                self._is_on = last_metric.state == 1
                self._extra_attrs["event_type"] = last_metric.type
                self._extra_attrs["event_date"] = last_metric.start
            else:
                self._is_on = False
            
            self._available = True

        except aiohttp.ClientError as err:
            self._available = False
            _LOGGER.error("Error updating Growappy Student %s: %s", self._student.name, err)
