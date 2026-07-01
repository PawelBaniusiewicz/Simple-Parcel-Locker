from dataclasses import dataclass
import secrets

@dataclass
class ActivationTokenService:

    @staticmethod
    def generate_activation_token(lenght: int) -> str:
        return secrets.token_urlsafe(lenght)
