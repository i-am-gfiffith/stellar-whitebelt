import test from 'node:test';
import assert from 'node:assert/strict';

import { buildNetworkConfig, formatBalance } from '../src/stellar';

test('buildNetworkConfig returns testnet defaults', () => {
  const config = buildNetworkConfig({});
  assert.equal(config.name, 'testnet');
  assert.equal(config.horizonUrl, 'https://horizon-testnet.stellar.org');
});

test('formatBalance preserves two decimal places', () => {
  assert.equal(formatBalance('10.5000'), '10.50');
  assert.equal(formatBalance('0'), '0.00');
});
