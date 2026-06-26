import * as dotenv from 'dotenv';
import { Keypair, Horizon, TransactionBuilder, Networks, BASE_FEE } from 'stellar-sdk';

dotenv.config();

export interface StellarConfig {
  name: string;
  horizonUrl: string;
  networkPassphrase: string;
}

export interface WalletInfo {
  publicKey: string;
  secretKey: string;
}

export interface BalanceInfo {
  assetCode: string;
  balance: string;
}

export function buildNetworkConfig(env: Record<string, string | undefined>): StellarConfig {
  const name = env.STELLAR_NETWORK ?? process.env.STELLAR_NETWORK ?? 'testnet';
  const horizonUrl = env.STELLAR_HORIZON_URL ?? process.env.STELLAR_HORIZON_URL ?? 'https://horizon-testnet.stellar.org';
  const networkPassphrase = name === 'public' ? Networks.PUBLIC : Networks.TESTNET;

  return { name, horizonUrl, networkPassphrase };
}

export function createWallet(): WalletInfo {
  const pair = Keypair.random();
  return { publicKey: pair.publicKey(), secretKey: pair.secret() };
}

export async function getBalances(publicKey: string, config: StellarConfig): Promise<BalanceInfo[]> {
  const server = new Horizon.Server(config.horizonUrl);
  const account = await server.loadAccount(publicKey);
  return account.balances.map((balance: any) => ({
    assetCode: balance.asset_code ?? 'XLM',
    balance: balance.balance,
  }));
}

export async function createAndSubmitTransaction(
  sourceSecret: string,
  destinationPublicKey: string,
  amount: string,
  config: StellarConfig,
): Promise<string> {
  const server = new Horizon.Server(config.horizonUrl);
  const sourceKeypair = Keypair.fromSecret(sourceSecret);
  const sourceAccount = await server.loadAccount(sourceKeypair.publicKey());
  const transactionBuilder = new TransactionBuilder(sourceAccount, {
    fee: BASE_FEE,
    networkPassphrase: config.networkPassphrase,
  })
    .addOperation(
      {
        destination: destinationPublicKey,
        asset: undefined,
        amount,
        type: 'payment',
      } as any,
    )
    .setTimeout(30);

  const transaction = transactionBuilder.build();
  transaction.sign(sourceKeypair);
  const result = await server.submitTransaction(transaction);
  return result.hash;
}

export function formatBalance(balance: string): string {
  const numeric = Number(balance);
  return Number.isFinite(numeric) ? numeric.toFixed(2) : '0.00';
}
