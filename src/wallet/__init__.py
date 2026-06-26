from __future__ import annotations

import base64
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.config import NetworkConfig, load_config
from src.utils import is_valid_address, is_valid_secret_seed


@dataclass(slots=True)
class Wallet:
    """A minimal Stellar-style wallet representation."""

    public_key: str
    secret_seed: Optional[str] = None
    network: Optional[NetworkConfig] = None

    @property
    def address(self) -> str:
        return self.public_key

    @property
    def secret_key(self) -> Optional[str]:
        return self.secret_seed

    @classmethod
    def generate(cls, network: Optional[NetworkConfig] = None) -> "Wallet":
        entropy = secrets.token_bytes(32)
        encoded = base64.b32encode(entropy).decode("ascii").rstrip("=")
        public_key = encoded[:56]
        secret_seed = encoded[:56]
        return cls(public_key=public_key, secret_seed=secret_seed, network=network)

    @classmethod
    def from_secret_seed(cls, secret_seed: str, network: Optional[NetworkConfig] = None) -> "Wallet":
        if not is_valid_secret_seed(secret_seed):
            raise ValueError("Secret seed must look like a Stellar seed")
        public_key = secret_seed.replace("S", "G", 1) if secret_seed.startswith("S") else secret_seed
        return cls(public_key=public_key, secret_seed=secret_seed, network=network)

    @classmethod
    def from_public_key(cls, public_key: str, network: Optional[NetworkConfig] = None) -> "Wallet":
        if not is_valid_address(public_key):
            raise ValueError("Public key must look like a Stellar address")
        return cls(public_key=public_key, secret_seed=None, network=network)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "public_key": self.public_key,
            "secret_seed": self.secret_seed,
            "network": None if self.network is None else self.network.network_name,
        }

    def sign(self, payload: Any) -> str:
        if self.secret_seed is None:
            raise ValueError("Wallet has no secret seed")
        return f"signed::{self.secret_seed}::{payload}"


def create_wallet(network: Optional[NetworkConfig] = None) -> Wallet:
    """Create a new wallet using the provided network config."""

    config = network or load_config()
    return Wallet.generate(network=config)
