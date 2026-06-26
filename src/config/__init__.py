from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(slots=True)
class NetworkConfig:
    """Configuration for a Stellar-style network."""

    horizon_url: str = "https://horizon-testnet.stellar.org"
    network_passphrase: str = "Test SDF Network ; September 2015"
    network_name: str = "testnet"

    def is_testnet(self) -> bool:
        return self.network_name.lower() in {"testnet", "test"}

    def is_public(self) -> bool:
        return self.network_name.lower() in {"public", "mainnet"}


def load_config(values: Optional[Mapping[str, Any]] = None) -> NetworkConfig:
    """Load config from the provided mapping or environment variables."""

    if values is None:
        values = {}
    horizon_url = str(values.get("HORIZON_URL") or values.get("horizon_url") or os.getenv("STELLAR_HORIZON_URL") or "https://horizon-testnet.stellar.org")
    network_passphrase = str(values.get("NETWORK_PASSPHRASE") or values.get("network_passphrase") or os.getenv("STELLAR_NETWORK_PASSPHRASE") or "Test SDF Network ; September 2015")
    network_name = str(values.get("NETWORK_NAME") or values.get("network_name") or os.getenv("STELLAR_NETWORK_NAME") or "testnet")
    return NetworkConfig(
        horizon_url=horizon_url,
        network_passphrase=network_passphrase,
        network_name=network_name,
    )
