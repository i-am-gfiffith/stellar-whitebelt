from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from src.utils import normalize_amount


@dataclass(slots=True)
class BalanceEntry:
    """Simple representation of a balance entry."""

    asset_type: str
    balance: str
    asset_code: Optional[str] = None
    asset_issuer: Optional[str] = None
    limit: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "asset_type": self.asset_type,
            "balance": self.balance,
        }
        if self.asset_code is not None:
            payload["asset_code"] = self.asset_code
        if self.asset_issuer is not None:
            payload["asset_issuer"] = self.asset_issuer
        if self.limit is not None:
            payload["limit"] = self.limit
        return payload


def parse_balance_entry(entry: Dict[str, Any]) -> BalanceEntry:
    """Create a BalanceEntry from a balance dict."""

    if not isinstance(entry, dict):
        raise TypeError("Balance entries must be mappings")
    asset_type = str(entry.get("asset_type", "native"))
    balance = str(entry.get("balance", "0"))
    return BalanceEntry(
        asset_type=asset_type,
        balance=balance,
        asset_code=entry.get("asset_code"),
        asset_issuer=entry.get("asset_issuer"),
        limit=entry.get("limit"),
    )


def get_native_balance(account_data: Dict[str, Any]) -> Optional[str]:
    """Return the native balance for an account payload if present."""

    balances = account_data.get("balances") if isinstance(account_data, dict) else None
    if not isinstance(balances, Iterable):
        return None
    for balance in balances:
        if not isinstance(balance, dict):
            continue
        if str(balance.get("asset_type", "")).lower() == "native":
            return str(balance.get("balance", "0"))
    return None


def summarize_balances(balances: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize balances by asset type and total balance."""

    totals: Dict[str, Any] = {}
    for raw_balance in balances:
        parsed = parse_balance_entry(raw_balance)
        key = parsed.asset_code or parsed.asset_type
        current = totals.get(key, 0.0)
        totals[key] = normalize_amount(current) + normalize_amount(parsed.balance)
    return totals
