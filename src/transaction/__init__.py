from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.utils import normalize_amount


@dataclass(slots=True)
class Transaction:
    """A small Stellar-style payment transaction representation."""

    source_account: str
    destination: str
    amount: str
    sequence: int = 1
    fee: int = 100
    memo: Optional[str] = None
    network_passphrase: Optional[str] = None
    signatures: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_account": self.source_account,
            "destination": self.destination,
            "amount": self.amount,
            "sequence": self.sequence,
            "fee": self.fee,
            "memo": self.memo,
            "network_passphrase": self.network_passphrase,
            "signatures": list(self.signatures),
        }


def build_payment_transaction(
    source_account: str,
    destination: str,
    amount: Any,
    sequence: int = 1,
    fee: int = 100,
    memo: Optional[str] = None,
    network_passphrase: Optional[str] = None,
) -> Transaction:
    """Create a payment transaction from the given values."""

    return Transaction(
        source_account=source_account,
        destination=destination,
        amount=str(normalize_amount(amount)),
        sequence=sequence,
        fee=fee,
        memo=memo,
        network_passphrase=network_passphrase,
    )


def sign_transaction(transaction: Transaction, signer: Any) -> Transaction:
    """Append a signature for the transaction."""

    if not isinstance(transaction, Transaction):
        raise TypeError("transaction must be a Transaction")
    signature = getattr(signer, "sign", None)
    if callable(signature):
        value = signature(transaction.to_dict())
    elif hasattr(signer, "public_key"):
        value = f"sig::{signer.public_key}"
    else:
        value = "signature"
    transaction.signatures.append(str(value))
    return transaction


def serialize_transaction(transaction: Transaction) -> str:
    """Serialize a transaction to a JSON string."""

    return json.dumps(transaction.to_dict(), sort_keys=True)
