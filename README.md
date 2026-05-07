# Waks - Bitcoin Miner with Calculator

A comprehensive Bitcoin mining application with real-time currency conversion and mining statistics dashboard.

## Features

✅ **Bitcoin Mining Engine**
- CPU-based mining with adjustable difficulty
- Multi-threaded mining for better performance
- Real-time hash rate calculation
- Mining statistics and analytics

✅ **Bitcoin to Real Money Calculator**
- Convert BTC to multiple currencies (USD, EUR, GBP, JPY, etc.)
- Real-time exchange rates via CoinGecko API
- Historical price tracking
- Profit/Loss calculations

✅ **Mining Pool Support**
- Stratum protocol implementation
- Connect to popular pools (Stratum.Mining, NiceHash, etc.)
- Pool statistics and share tracking

✅ **Web Dashboard**
- Real-time monitoring
- Mining statistics and analytics
- Currency conversion tools
- Configuration management

✅ **Advanced Features**
- Hardware acceleration support (GPU mining ready)
- Automatic difficulty adjustment
- Mining history and logs
- Performance optimization
- Multi-currency support

## Project Structure

```
Waks/
├── core/                      # Core mining engine
│   ├── miner.py              # Main mining logic
│   ├── blockchain.py         # Blockchain utilities
│   └── hash_engine.py        # Hash computation
├── calculator/               # Calculator module
│   ├── converter.py          # Bitcoin to fiat converter
│   ├── rates.py              # Exchange rate fetcher
│   └── profit_calculator.py  # Profit/loss calculations
├── pool/                     # Mining pool support
│   ├── stratum.py           # Stratum protocol
│   └── pool_manager.py      # Pool connection manager
├── web/                      # Web dashboard
│   ├── app.py               # Flask application
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, assets
├── config/                   # Configuration files
│   └── settings.json        # Default settings
├── tests/                    # Unit tests
├── requirements.txt         # Python dependencies
├── main.py                  # Entry point
└── config_template.json     # Configuration template
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ashermohamed546-arch/Waks.git
cd Waks
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure settings:
```bash
cp config_template.json config.json
# Edit config.json with your settings
```

## Usage

### CPU Mining
```bash
python main.py --mode cpu --threads 4
```

### Mine with Pool
```bash
python main.py --mode pool --pool stratum.mining.com --port 3333 --worker username.worker1
```

### Start Web Dashboard
```bash
python main.py --web --port 5000
# Open http://localhost:5000 in your browser
```

### Run Calculator Only
```bash
python -m calculator.converter --amount 0.5 --currency USD
```

## Configuration

Edit `config.json` for:
- Mining threads
- Pool credentials
- Currency preferences
- Wallet address
- Difficulty level
- Update frequency for rates

## Mining Algorithms Supported

- SHA-256 (Bitcoin)
- Scrypt (Litecoin compatible)
- Custom difficulty levels

## Calculator Features

- **Real-time Conversion**: Get live BTC to fiat rates
- **Historical Data**: Track price history
- **Portfolio Value**: Calculate total portfolio worth
- **Mining Profit**: Estimate earnings based on hash rate
- **ROI Calculator**: Calculate return on investment

## Web Dashboard

Access the web interface for:
- **Mining Status**: Current hash rate, shares, difficulty
- **Earnings**: Real-time earnings in multiple currencies
- **Charts**: Hash rate, earnings, difficulty trends
- **Settings**: Configure mining parameters
- **Calculator**: Convert BTC to any currency

## API Endpoints

- `GET /api/mining/stats` - Current mining statistics
- `GET /api/mining/history` - Mining history
- `GET /api/calculator/convert` - Convert BTC to fiat
- `GET /api/calculator/rates` - Get exchange rates
- `GET /api/mining/hashrate` - Current hash rate
- `POST /api/mining/config` - Update mining configuration

## Performance

- **CPU Mining**: 1-5 MH/s per core (hardware dependent)
- **GPU Mining**: 100+ MH/s (with compatible hardware)
- **Web Dashboard**: Lightweight, <50MB memory usage

## Supported Currencies

USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, SEK, NZD, MXN, SGD, HKD, NOK, KRW, TRY, RUB, INR, BRL, ZAR

## Mining Pools

- Stratum.Mining (stratum.mining.com)
- NiceHash (stratum-mining.nicehash.com)
- F2Pool (stratum.f2pool.com)
- Slush Pool (stratum.slushpool.com)
- Custom Stratum servers

## Security

⚠️ **Important Security Notes**:
- Never share your mining wallet address publicly
- Keep your worker credentials secure
- Use HTTPS for remote dashboard access
- Rotate pool credentials regularly
- Monitor for unusual activity

## Troubleshooting

### Low Hash Rate
- Check CPU/GPU utilization
- Increase thread count
- Verify difficulty settings
- Check for thermal throttling

### Connection Issues
- Verify pool address and port
- Check firewall settings
- Test internet connectivity
- Review logs for error messages

### Calculator Not Updating
- Check API rate limits (CoinGecko)
- Verify internet connection
- Check for API service outages
- Increase update interval

## License

MIT License

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Support

For issues, questions, or suggestions, please create an issue on GitHub.

## Disclaimer

Bitcoin mining consumes significant electricity. Before starting:
- Calculate electricity costs vs. potential earnings
- Check local regulations
- Ensure adequate cooling for hardware
- Use only dedicated hardware for mining

## Roadmap

- [ ] GPU mining support (CUDA/OpenCL)
- [ ] ASIC mining support
- [ ] Advanced pool management
- [ ] Mobile app
- [ ] Machine learning for optimization
- [ ] Multi-algorithm support
- [ ] Cloud mining integration
- [ ] Telegram bot notifications
