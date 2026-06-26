import { createWallet, buildNetworkConfig, getBalances, createAndSubmitTransaction, formatBalance } from './stellar';

async function main(): Promise<void> {
  const command = process.argv[2] ?? 'wallet';
  const config = buildNetworkConfig(process.env);

  if (command === 'wallet') {
    const wallet = createWallet();
    console.log('Wallet created successfully.');
    console.log(`Public key: ${wallet.publicKey}`);
    console.log(`Secret key: ${wallet.secretKey}`);
    return;
  }

  if (command === 'balance') {
    const publicKey = process.env.STELLAR_PUBLIC_KEY;
    if (!publicKey) {
      console.error('Set STELLAR_PUBLIC_KEY in your environment to fetch balances.');
      process.exit(1);
    }
    console.log(`Fetching balances from ${config.horizonUrl}...`);
    const balances = await getBalances(publicKey, config);
    for (const balance of balances) {
      console.log(`${balance.assetCode}: ${formatBalance(balance.balance)}`);
    }
    return;
  }

  if (command === 'tx') {
    const secret = process.env.STELLAR_SECRET_KEY;
    const destination = process.env.STELLAR_DESTINATION;
    const amount = process.env.STELLAR_AMOUNT ?? '1';
    if (!secret || !destination) {
      console.error('Set STELLAR_SECRET_KEY and STELLAR_DESTINATION to submit a transaction.');
      process.exit(1);
    }
    console.log('Submitting a test transaction...');
    const hash = await createAndSubmitTransaction(secret, destination, amount, config);
    console.log(`Transaction hash: ${hash}`);
    return;
  }

  console.log('Usage: npm run wallet:create | npm run balance | npm run tx:demo');
}

main().catch((error) => {
  console.error('Error:', error instanceof Error ? error.message : error);
  process.exit(1);
});
