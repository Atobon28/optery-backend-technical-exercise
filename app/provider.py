import time
import uuid


class ExternalProviderError(Exception):
    pass


class ExternalProvider:
    """Small fake provider used by the interview exercise."""

    def __init__(self):
        self.calls: list[dict] = []

    def remove(self, email: str, provider: str) -> str:
        # Simulate an external request that has a visible side effect.
        time.sleep(0.05)
        reference = f"ext-{uuid.uuid4()}"
        self.calls.append({"email": email, "provider": provider, "reference": reference})
        return reference


provider_client = ExternalProvider()
