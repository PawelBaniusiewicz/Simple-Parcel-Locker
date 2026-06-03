from dataclasses import dataclass
import secrets

@dataclass
class ActivationTokenService:

    @staticmethod
    def generate_activation_token() -> str:
        return secrets.token_urlsafe(32)
