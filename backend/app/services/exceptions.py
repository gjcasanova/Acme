from app.models.enums import ProviderName


class InvalidApiKeyError(Exception):
    """Raised when the API key is missing, malformed, unknown, or belongs to an inactive user."""


class VehicleNotFoundError(Exception):
    """Raised when a provider's external id does not match any vehicle."""

    def __init__(self, provider: ProviderName) -> None:
        self.provider = provider
        super().__init__(f"Vehicle not found for provider {provider.value}")
