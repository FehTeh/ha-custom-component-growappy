"""The Growappy integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.growappy import GROWAPPY
from .coordinator import GrowappyUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.DEVICE_TRACKER
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Growappy from a config entry."""
    
    # 1. Initialize the API client using HA's shared session
    session = async_get_clientsession(hass)
    api = GROWAPPY(session)
    
    # 2. Create the Data Coordinator
    coordinator = GrowappyUpdateCoordinator(hass, api, entry)
    
    # 3. Trigger the first data refresh
    # This ensures we have student data before loading platforms
    await coordinator.async_config_entry_first_refresh()

    # 4. Store the coordinator for platforms to access
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # 5. Set up all defined platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload all platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # Clean up stored data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
