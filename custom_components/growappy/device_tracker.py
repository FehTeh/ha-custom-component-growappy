from homeassistant.components.device_tracker import TrackerEntity, SourceType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .entity import GrowappyDevice # Import your base class

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Growappy tracker platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Map entities using the data stored in coordinator
    async_add_entities(
        GrowappyStudentTracker(coordinator, student) 
        for student in coordinator.data["students"]
    )

class GrowappyStudentTracker(CoordinatorEntity, GrowappyDevice, TrackerEntity):
    """Representation of a student as a device tracker."""

    def __init__(self, coordinator, student):
        """Initialize the tracker."""
        # 1. Initialize the CoordinatorEntity (handles updates)
        CoordinatorEntity.__init__(self, coordinator)
        
        # 2. Initialize your custom GrowappyDevice (handles device info/API)
        # Assuming GrowappyDevice.__init__ takes (api, student)
        GrowappyDevice.__init__(self, coordinator.api, student)

        self._student = student
        
        # Unique ID for the tracker platform
        self._attr_unique_id = f"{DOMAIN}_{student.id}_tracker"
        
        # If your GrowappyDevice class sets self._attr_device_info, 
        # this tracker will be grouped under the same device in the UI.

    @property
    def name(self) -> str:
        """Return the name of the student."""
        return self._student.full_name

    @property
    def translation_key(self) -> str:
        """Return the translation key for the device tracker."""
        return "student_presence"

    @property
    def location_name(self) -> str:
        """Return the state key."""
        metric = self.coordinator.data["metrics"].get(self._student.id)
        
        if metric and metric.state == 1:
            return "at_school"
        return "not_home"

    @property
    def source_type(self) -> SourceType:
        """The source of the tracking information."""
        return SourceType.ROUTER

    @property
    def icon(self) -> str:
        """Icon to use in the frontend."""
        return "mdi:school"

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes from coordinator data."""
        metric = self.coordinator.data["metrics"].get(self._student.id)
        attrs = {}
        
        if metric:
            attrs.update({
                "event_type": metric.type,
                "check_in_time": metric.start,
                "student_id": self._student.id
            })
            
        return attrs
