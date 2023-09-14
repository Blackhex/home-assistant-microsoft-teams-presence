"""The Microsoft Teams Presence integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse

from .const import DOMAIN, LOGGER, PLATFORMS as MY_PLATFORMS

PLATFORMS: list[Platform] = MY_PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    LOGGER.info("In async_setup_entry()")

    async def async_handle_test(call: ServiceCall) -> ServiceResponse:
        """Handle the service call."""
        LOGGER.info("In handle_test(data='%s')", call.data)

        # hass.states.set("test.data", call.data)

        return call.data

    hass.services.async_register(DOMAIN, "test", async_handle_test)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
