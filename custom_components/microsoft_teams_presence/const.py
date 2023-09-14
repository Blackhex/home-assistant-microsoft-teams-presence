"""Constants for the Microsoft Teams Presence integration."""
import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "microsoft_teams_presence"
PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]

# Update with your own urls
# _TODO: Request the tenant ID together with client ID and client secret.
OAUTH2_APP_TENANT = "7b24ae4e-c22e-48e7-b546-677be914614c"
OAUTH2_AUTHORIZE_URL = (
    f"https://login.microsoftonline.com/{OAUTH2_APP_TENANT}/oauth2/v2.0/authorize"
)
OAUTH2_TOKEN_URL = (
    f"https://login.microsoftonline.com/{OAUTH2_APP_TENANT}/oauth2/v2.0/token"
)
OAUTH2_REDIRECT_URL = "https://my.home-assistant.io/redirect/oauth"
OAUTH2_SCOPES = ["User.Read", "Presence.Read.All"]
# OAUTH2_SCOPES = ["api://d3e5292c-d99f-4025-b580-7527f85738c2/User.Read", "api://d3e5292c-d99f-4025-b580-7527f85738c2/Presence.Read.All"]

LOGGER = logging.getLogger(__package__)
