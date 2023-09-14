"""Config flow for Microsoft Teams Presence."""
import logging
from typing import Any, Optional

from azure.core.credentials import AccessToken
from azure.identity import AuthorizationCodeCredential, OnBehalfOfCredential
from msgraph import GraphServiceClient

from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN, LOGGER, OAUTH2_APP_TENANT, OAUTH2_REDIRECT_URL, OAUTH2_SCOPES


class TeamsPresenceConfigFlow(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Microsoft Teams Presence integration config flow."""

    VERSION = 1
    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return the default logger."""
        return LOGGER

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "tenant": OAUTH2_APP_TENANT,
            "grant_type": "client_credentials",
            "scope": " ".join(OAUTH2_SCOPES),
        }

    # _TODO: Implement re-authentication https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#configuration-via-oauth2
    async def async_oauth_create_entry(self, data: dict) -> FlowResult:
        """Create an oauth config entry."""

        # user = await self._test(data)

        # self.logger.info("User presence: %s", user)

        return await super().async_oauth_create_entry(data)

    async def _test(self, data):
        return await self._test_custom_credential(data)

    async def _test_custom_credential(self, data):
        self.logger.info("test_custom_credential()")

        access_token = data["token"]["access_token"]
        expires_at = data["token"]["expires_at"]

        self.logger.info("Access token: %s", access_token)

        credential = CustomCredential(access_token, expires_at)
        graph_client = GraphServiceClient(credentials=credential)
        # return await graph_client.users.by_user_id("1ecbd423-b0cc-4955-925a-589859e8d58b").presence.get()
        return await graph_client.communications.presences.get()

    async def _test_authorization_code_credential(self, data):
        access_token = data["token"]["access_token"]

        self.logger.info("Access token: %s", access_token)

        credential = AuthorizationCodeCredential(
            tenant_id=OAUTH2_APP_TENANT,
            client_id="<client_id>",
            authorization_code=access_token,
            redirect_uri=OAUTH2_REDIRECT_URL,
        )
        graph_client = GraphServiceClient(
            credentials=credential, scopes=["https://graph.microsoft.com/.default"]
        )
        return await graph_client.me.presence.get()

    async def _test_on_behalf_of_credential(self, data):
        access_token = data["token"]["access_token"]

        self.logger.info("Access token: %s", access_token)

        credential = OnBehalfOfCredential(
            tenant_id=OAUTH2_APP_TENANT,
            client_id="<client_id>",
            client_secret="<client_secret>",
            user_assertion=access_token,
        )

        graph_client = GraphServiceClient(credentials=credential)
        return await graph_client.me.presence.get()


class CustomCredential:
    """Custom implementation of access token credentials."""

    def __init__(self, access_token: str, expires_in: float) -> None:
        """Save the token to the instance."""
        self._access_token = AccessToken(access_token, round(expires_in))

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        **kwargs: Any,
    ) -> AccessToken:
        """Just returns the access token."""
        return self._access_token
