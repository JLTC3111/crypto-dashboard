# Portfolio Restructuring Guide

## Overview
The Portfolio Restructuring System allows you to properly track asset switches and cost basis transfers when you've restructured your portfolio multiple times. This addresses the common scenario where you've sold one asset to buy another, but want to track the overall performance as if it's one continuous investment strategy.

## Key Features

### 1. **Transaction Types**
- **BUY**: Standard purchase (default)
- **SELL**: Standard sale (default)
- **RESTRUCTURE_OUT**: Asset sold as part of restructuring (excluded from portfolio value)
- **RESTRUCTURE_IN**: Asset bought with proceeds from restructuring (cost basis adjusted)
- **TRANSFER**: Direct asset-to-asset transfer
- **EXCLUDE**: Manually excluded from all calculations

### 2. **Cost Basis Transfer**
When you restructure, the system can transfer the cost basis from your old assets to new assets, allowing you to calculate breakeven prices based on your original investment rather than current market prices.

### 3. **Restructuring Groups**
Link related transactions together (e.g., selling BTC to buy ETH) so the system knows they're part of the same restructuring event.

## How to Use

### Basic Mode (Simple Buy/Sell)
1. Keep the "Advanced Mode" checkbox unchecked in the sidebar
2. Use normal "Buy" and "Sell" transaction types
3. All transactions count toward portfolio value

### Advanced Mode (Restructuring)
1. ✅ Check "Advanced Mode (Restructuring)" in the sidebar
2. Select appropriate transaction types:
   - Use **RESTRUCTURE_OUT** for assets you're selling as part of portfolio restructuring
   - Use **RESTRUCTURE_IN** for assets you're buying with those proceeds
3. Create or join restructuring groups to link related transactions

### Step-by-Step Restructuring Process

#### Scenario: You bought BTC for $10,000, it went to $15,000, then you sold it all to buy ETH

**Step 1: Mark the BTC sale as RESTRUCTURE_OUT**
1. Enable Advanced Mode
2. Select "RESTRUCTURE_OUT" as transaction type
3. Enter BTC sale details (negative quantity)
4. Create a new restructuring group (e.g., "BTC-to-ETH-Q1-2024")

**Step 2: Mark the ETH purchase as RESTRUCTURE_IN**
1. Select "RESTRUCTURE_IN" as transaction type
2. Enter ETH purchase details (positive quantity)
3. Join the same restructuring group

**Result:**
- BTC sale won't count toward your current portfolio value
- ETH purchase will have its cost basis adjusted to reflect your original $10,000 BTC investment
- Breakeven calculation for ETH will be based on $10,000, not the ETH purchase price

### Using the Restructuring Tab

Navigate to **Portfolio Management → 🔄 Restructuring** tab for:

1. **Portfolio Status Overview**
   - See how many transactions are included/excluded
   - View total cost basis transferred
   - Monitor restructuring impact

2. **Mark Existing Transactions**
   - Retroactively mark transactions as RESTRUCTURE_OUT
   - Bulk update transaction types

3. **Create Restructuring Groups**
   - Link related transactions
   - Add descriptions for audit trail

4. **View by Transaction Type**
   - See all transactions organized by type
   - Verify restructuring logic is correct

## Examples

### Example 1: Simple Asset Switch
**Original Portfolio:**
- Bought 1 BTC @ $40,000
- BTC now worth $50,000
- Sell BTC, buy 20 ETH @ $2,500 each

**Without Restructuring:**
- ETH breakeven: $2,500
- Need ETH to reach $2,500+ to be profitable

**With Restructuring:**
1. Mark BTC sale as RESTRUCTURE_OUT (group: "BTC-ETH-Switch")
2. Mark ETH buy as RESTRUCTURE_IN (same group)
3. ETH breakeven becomes: $40,000 ÷ 20 = $2,000
4. Already profitable since ETH > $2,000

### Example 2: Multiple Restructuring Events
**Timeline:**
1. Buy BTC @ $30,000
2. BTC → ETH @ $35,000 BTC value
3. ETH → SOL @ $40,000 ETH value
4. Want to track overall performance from original $30,000

**Setup:**
1. Group 1: "BTC-ETH" (RESTRUCTURE_OUT BTC, RESTRUCTURE_IN ETH)
2. Group 2: "ETH-SOL" (RESTRUCTURE_OUT ETH, RESTRUCTURE_IN SOL)
3. SOL cost basis = $30,000 (original investment)

## Portfolio Summary Changes

The Portfolio Summary section now shows:
- **Adjusted cost basis** (accounting for transfers)
- **Excluded transactions count** (restructured-out assets)
- **Cost basis transferred amount**
- **Warning indicators** when restructuring is active

## Best Practices

1. **Create Groups Before Transactions**
   - Set up restructuring groups first
   - Assign transactions to groups as you add them

2. **Document Your Strategy**
   - Use descriptive group names
   - Add descriptions explaining the restructuring logic

3. **Verify Calculations**
   - Check the Restructuring tab to ensure proper grouping
   - Verify cost basis transfers are correct

4. **Consistent Timeframes**
   - Group transactions that happen close together
   - Don't mix unrelated restructuring events

## Troubleshooting

### "My portfolio value seems wrong"
- Check if transactions are properly marked as RESTRUCTURE_OUT
- Verify restructuring groups are set up correctly
- Look for transactions that should be excluded

### "Cost basis not transferring"
- Ensure OUT and IN transactions are in the same group
- Check that the group is properly saved
- Verify transaction types are correct

### "Breakeven prices don't make sense"
- Review the cost basis transfer calculations
- Check if multiple restructuring events are conflicting
- Verify the original purchase prices

## Database Schema

New columns added to support restructuring:
- `transaction_type`: Enum for transaction classification
- `include_in_portfolio`: Boolean for portfolio value calculations
- `adjusted_purchase_price`: Price after cost basis transfer
- `original_purchase_price`: Original purchase price
- `cost_basis_transferred`: Amount transferred from other assets
- `restructure_group`: Links related transactions

## Migration

Existing transactions will:
- Default to "BUY" or "SELL" based on quantity sign
- Be included in portfolio calculations (backward compatible)
- Can be retroactively marked for restructuring using the management interface
