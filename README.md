# Stellar White Belt

This project is a simple Stellar testnet starter that demonstrates wallet creation, balance checks, and a first transaction workflow.

## Features
- Generate a new Stellar wallet keypair
- Connect to the Stellar testnet Horizon API
- Retrieve account balances
- Build and submit a basic payment transaction

## Setup
1. Install Node.js 20+ and npm.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a local environment file:
   ```bash
   cp .env.example .env
   ```
4. Fill in the required values in `.env`.

## Usage
- Create a wallet:
  ```bash
  npm run wallet:create
  ```
- Check balances:
  ```bash
  npm run balance
  ```
- Submit a sample transaction:
  ```bash
  npm run tx:demo
  ```

## Notes
- Never commit your `.env` file or secret keys to GitHub.
- Fund the wallet on testnet before sending a real transaction.
