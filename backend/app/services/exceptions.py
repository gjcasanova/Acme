class InvalidApiKeyError(Exception):
    """Raised when the API key is missing, malformed, unknown, or belongs to an inactive user."""
