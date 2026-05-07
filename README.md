# Waks - Bitcoin Miner with Calculator & Mobile Money Transfer

## Overview

**Waks** is a comprehensive Bitcoin mining application with integrated calculator and **mobile money transfer capabilities** for withdrawing earnings directly to mobile wallets in Africa and beyond.

### Key Features

✅ **Bitcoin Mining Engine**
- CPU-based mining with adjustable difficulty
- Multi-threaded mining for optimal performance
- Real-time hash rate calculation
- Mining statistics and analytics

✅ **Bitcoin to Real Money Calculator**
- Convert BTC to multiple currencies
- **Full support for African currencies** including Ugandan Shilling (UGX), Kenyan Shilling (KES), Nigerian Naira (NGN), etc.
- Real-time exchange rates via CoinGecko API
- Historical price tracking
- Profit/Loss calculations

✅ **🌍 Mobile Money Transfer (NEW!)**
- **Withdraw mining earnings directly to mobile wallets**
- **Supported Providers:**
  - **MTN Mobile Money** (Uganda, Ghana, Kenya, Nigeria, Cameroon)
  - **Airtel Money** (Uganda, Kenya, Tanzania, Nigeria)
  - **Uganda Telecom Money** (Uganda)
  - **Orange Money** (Egypt, Ivory Coast, Cameroon)
  - **Vodafone Cash** (Ghana, Egypt)
  - **Safaricom M-Pesa** (Kenya, Tanzania)
  - **Equitel** (Kenya)

- **Supported Currencies for Transfer:**
  - 🇺🇬 **UGX** - Ugandan Shilling (MTN, Airtel, UTL)
  - 🇰🇪 **KES** - Kenyan Shilling (Safaricom, Airtel)
  - 🇬🇭 **GHS** - Ghanaian Cedi (MTN, Airtel, Vodafone)
  - 🇳🇬 **NGN** - Nigerian Naira (MTN, Airtel)
  - 🇪🇬 **EGP** - Egyptian Pound (Orange, Vodafone)

✅ **Mining Pool Support**
- Stratum protocol implementation
- Connect to popular pools
- Pool statistics and share tracking

✅ **Web Dashboard**
- Real-time monitoring
- Mining statistics and analytics
- Currency conversion tools
- Configuration management

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/ashermohamed546-arch/Waks.git
cd Waks

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp config_template.json config.json
```

## Usage

### CPU Mining
```bash
python main.py --mode cpu --threads 4
```

### Mining with Pool
```bash
python main.py --mode pool --pool stratum.mining.com --port 3333 --worker username.worker1
```

### Web Dashboard
```bash
python main.py --web --port 5000
# Open http://localhost:5000
```

### Bitcoin Calculator
```bash
# Convert to specific currency
python main.py --calculator --amount 0.5 --currency USD

# Interactive mode
python main.py --calculator
```

### 🌍 Mobile Money Transfer

#### Check Available Providers
```bash
python main.py --mobile-money --providers
```

#### Send to Mobile Wallet (Uganda - Ugandan Shilling)
```bash
python main.py --mobile-money --btc 0.1 --phone +256700123456 --provider MTN --currency UGX
```

#### Send to Mobile Wallet (Kenya - Kenyan Shilling)
```bash
python main.py --mobile-money --btc 0.05 --phone +254712345678 --provider SAFARICOM --currency KES
```

#### Send to Multiple Currencies
```bash
# Ghana
python main.py --mobile-money --btc 0.1 --phone +233501234567 --provider MTN --currency GHS

# Nigeria
python main.py --mobile-money --btc 0.15 --phone +2348012345678 --provider MTN --currency NGN

# Egypt
python main.py --mobile-money --btc 0.08 --phone +201001234567 --provider ORANGE --currency EGP
```

#### Check Transfer Status
```bash
python main.py --mobile-money --status TX-ABC123DEF456
```

#### View Transfer History
```bash
python main.py --mobile-money --history
```

## Mobile Money Features

### Transfer Fees
- **MTN Mobile Money**: 2%
- **Airtel Money**: 2%
- **Uganda Telecom**: 2.5%
- **Orange Money**: 2%
- **Safaricom M-Pesa**: 2.5%

### Transfer Limits
- **Minimum**: $0.50 - $1.00 equivalent
- **Maximum**: $300 - $500 equivalent
- Exact limits vary by provider and country

### How It Works

1. **Check Available Providers**
   ```bash
   python main.py --mobile-money --providers
   ```

2. **Initiate Transfer**
   ```bash
   python main.py --mobile-money --btc 0.1 --phone +256700000000 --provider MTN --currency UGX
   ```

3. **Confirm on Mobile Wallet**
   - You'll receive a prompt on your mobile wallet
   - Confirm the transaction amount and details

4. **Track Status**
   ```bash
   python main.py --mobile-money --status [transaction-id]
   ```

5. **Funds Deposited**
   - Funds are deposited to your mobile wallet account
   - No intermediaries or bank accounts needed!

## Supported Currencies

### All Calculator Currencies
USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, INR, SEK, NZD, MXN, SGD, HKD, NOK, KRW, TRY, BRL, ZAR

### Mobile Money Transfer Currencies
🇺🇬 UGX, 🇰🇪 KES, 🇬🇭 GHS, 🇳🇬 NGN, 🇪🇬 EGP

## Project Structure

```
Waks/
├── core/                      # Core mining engine
│   ├── miner.py              # Main mining logic
│   ├── blockchain.py         # Blockchain utilities
│   ├── hash_engine.py        # Hash computation
│   └── utils.py              # Helper functions
├── calculator/                # Calculator & mobile money
│   ├── converter.py          # BTC to fiat converter
│   ├── rates.py              # Exchange rate fetcher
│   ├── profit_calculator.py  # Profit/loss calculations
│   └── mobile_money.py       # Mobile money transfers ✨
├── pool/                      # Mining pool support
├── web/                       # Web dashboard
├── config_template.json       # Configuration template
├── main.py                    # Entry point
└── requirements.txt           # Dependencies
```

## API Endpoints

- `GET /api/mining/stats` - Mining statistics
- `GET /api/mining/history` - Mining history
- `GET /api/calculator/convert` - Convert BTC to fiat
- `POST /api/mobile-money/transfer` - Initiate transfer
- `GET /api/mobile-money/status/:id` - Check status
- `GET /api/mobile-money/history` - Transfer history

## Security Considerations

⚠️ **Important**
- Keep your private keys secure
- Never share worker credentials
- Use HTTPS for remote access
- Validate phone numbers before transfer
- Store transaction records safely

## Troubleshooting

### Mobile Money Issues

**Transfer Fails**
- Verify phone number format
- Check provider support for your country
- Ensure sufficient balance
- Check transfer limits

**Provider Not Found**
```bash
python main.py --mobile-money --providers
```

**Wrong Amount**
- Transfer fees are deducted automatically
- Use correct BTC amount
- Exchange rates update every 5 minutes

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## License

MIT License - Free for personal and commercial use

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation

## Disclaimer

Bitcoin mining uses significant electricity. Calculate costs vs. earnings first!

---

**Made with ❤️ for Bitcoin miners in Africa and worldwide**
