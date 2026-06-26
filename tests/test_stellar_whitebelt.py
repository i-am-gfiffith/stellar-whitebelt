from balance import parse_balance_entry, summarize_balances
from config import load_config
from transaction import build_payment_transaction, serialize_transaction, sign_transaction
from wallet import Wallet


def test_config_defaults():
    config = load_config({})
    assert config.network_name == "testnet"
    assert config.horizon_url.startswith("https://")


def test_wallet_generation_and_signing():
    wallet = Wallet.generate()
    assert wallet.public_key
    assert wallet.secret_seed

    tx = build_payment_transaction("GABC", "GXYZ", "10", sequence=2, fee=200)
    signed = sign_transaction(tx, wallet)
    assert len(signed.signatures) == 1
    assert serialize_transaction(signed)


def test_balance_parsing_and_summary():
    entry = parse_balance_entry({"asset_type": "native", "balance": "10"})
    assert entry.balance == "10"

    summary = summarize_balances([
        {"asset_type": "native", "balance": "10"},
        {"asset_type": "credit_alphanum4", "asset_code": "USD", "balance": "5"},
    ])
    assert summary["native"] == 10
