from datetime import datetime, timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN
from .api.exceptions import GrowappyUnauthorizedException

_LOGGER = logging.getLogger(__name__)

class GrowappyUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Growappy API."""

    def __init__(self, hass, api, entry):
        """Initialize the coordinator."""
        self.api = api
        self.entry = entry
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Data will be refreshed every 5 minutes
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Fetch data from API (Runs periodically)."""
        config = self.entry.data
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # 1. Fetch the list of students
            students = await self.api.getStudents(config["access_token"])
            
            # 2. Fetch metrics (diary) for each student
            # We store it in a dictionary: { student_id: last_metric }
            data = {"students": students, "metrics": {}}
            
            for student in students:
                metrics = await self.api.getDiary(
                    config["access_token"], student.id, today, today
                )
                if metrics:
                    # Store the latest metric event
                    data["metrics"][student.id] = metrics[-1]
            
            return data

        except GrowappyUnauthorizedException:
            # 3. Centralized Token Refresh logic
            _LOGGER.info("Token expired, attempting to refresh...")
            try:
                new_token = await self.api.refreshToken(config["refresh_token"])
                new_data = {
                    **config, 
                    "access_token": new_token.access, 
                    "refresh_token": new_token.refresh
                }
                
                # Update the Config Entry with the new valid tokens
                self.hass.config_entries.async_update_entry(self.entry, data=new_data)
                
                # Retry the data update with the new token
                return await self._async_update_data()
            except GrowappyUnauthorizedException:
                # If refresh_token also fails, we need the user!
                _LOGGER.error("Refresh token is invalid. Re-auth required.")
                raise ConfigEntryAuthFailed("Refresh token expired. Please log in again.")
            except Exception as err:
                raise UpdateFailed(f"Refresh failed: {err}")
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Growappy API: {err}")