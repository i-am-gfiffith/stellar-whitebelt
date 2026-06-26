# White Belt Submission Notes

## Wallet creation proof
- Run `npm run wallet:create`
- Capture the public key and secret key output

## Balance retrieval proof
- Set `STELLAR_PUBLIC_KEY` in your environment
- Run `npm run balance`
- Capture the balance output from the Horizon testnet response

## Transaction proof
- Set `STELLAR_SECRET_KEY`, `STELLAR_DESTINATION`, and optionally `STELLAR_AMOUNT`
- Run `npm run tx:demo`
- Capture the resulting transaction hash

## Screenshots to capture
- Terminal output showing wallet creation
- Terminal output showing testnet balances
- Terminal output showing the submitted transaction hash
