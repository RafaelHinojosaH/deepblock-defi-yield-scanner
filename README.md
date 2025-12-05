# DeepBlockAI — DeFi Yield Scanner

A professional-grade yield discovery engine built to scan, filter, score, and rank yield opportunities across multiple chains using real-time data from **DeFiLlama**.  
This bot is part of the **DeepBlockAI Bot Suite**, powering analytics for the *DeepBlockAI Dashboard*.

---

## 🚀 Description

`deepblock-defi-yield-scanner` automatically:

- Fetches all pools from DeFiLlama.
- Applies risk and sustainability filters.
- Computes a proprietary **DeFiYieldScore (0–100)**.
- Ranks pools according to TVL, APY quality, and sustainability.
- Sends the Top N results to a Telegram channel.
- Exports structured JSON for consumption by **DeepBlockAI Dashboard**.
- Stores historical snapshots for analytics, monitoring, and backtesting.

Its purpose is to provide **clean, reliable, intelligence-ready yield insights** for DeFi investors and analysts.

---

## ✨ Features

- 🔍 Real-time DeFiLlama pool ingestion  
- 🧪 Custom scoring engine: APY normalization, sustainability weights, TVL logarithmic scaling  
- 📉 Risk filters: min TVL, max APY, allowed chains, APY decomposition  
- 📡 Telegram publishing  
- 📊 Dashboard JSON export (latest + historical)  
- 🗂 Clean architecture (sources → core → main → integrations)  
- 🧱 Fully modular and extensible  

---

## 🏗 Architecture Overview

```
defi-yield-scanner/
│
├── config/
│   └── settings.py         # Environment config and typed Settings dataclass
│
├── src/
│   ├── main.py             # Main execution pipeline
│   ├── core/
│   │   ├── filters.py      # Risk filters for APY, TVL, chains
│   │   ├── scoring.py      # DeFiYieldScore algorithm (0–100)
│   │   ├── formatting.py   # Telegram message formatting
│   │   ├── logger.py       # Custom logger
│   │   └── telegram_client.py
│   └── sources/
│       └── defillama_client.py  # Fetches raw pools from DeFiLlama API
│
├── storage/
│   ├── processed/          # JSON snapshots (auto-generated)
│   └── logs/               # Optional logs
│
└── .env.example            # Example environment file
```

---

## 🔧 Environment Variables (`.env`)

Create a file named `.env`:

```
ENV=local

TELEGRAM_BOT_TOKEN=123456789:XXXXXX
TELEGRAM_CHAT_ID=-123456789

MIN_TVL_USD=500000
MAX_APY=250
PREFERRED_CHAINS=Ethereum,Arbitrum,Base,Solana
TOP_N=10
```

### Explanation

| Variable | Description |
|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Channel/group/user ID |
| `MIN_TVL_USD` | Minimum pool TVL to consider |
| `MAX_APY` | APY limit to filter out degen pools |
| `PREFERRED_CHAINS` | Only yields on these chains |
| `TOP_N` | Number of pools to publish |

---

## ▶️ Usage

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Activate virtual environment (optional)

```bash
source venv/bin/activate
```

### 3) Run the scanner

```bash
python -m src.main
```

---

## 📊 Dashboard Integration

### Output files generated:

#### Historical snapshots:

```
storage/processed/defi-yield_YYYYMMDD_HHMMSS.json
```

#### Dashboard live feed:

```
../deepblockai-dashboard/data/defi-yield-latest.json
```

These JSON files power the **DeepBlockAI Dashboard**, enabling:

- Live yield rankings  
- Chain-level analytics  
- Score distributions  
- Historical trend visualizations  

The scanner also supports optional integration with `writer.py` inside `deepblockai-dashboard`:

```python
save_bot_payload("defi-yield-scanner", dashboard_items)
```

---

## 🛣 Roadmap

### 🔜 Short term
- Add multi-source yield aggregation (Llama + Pendle + Yearn)  
- Smart chain detection  
- Improved sustainability scoring  

### 🚧 Mid term
- Historical APY volatility weighting  
- Aggregated APY confidence score  
- Bridge risk scoring  

### 🔮 Long term
- Fully autonomous multi-bot DeepBlockAI index  
- AI-driven narrative detection  
- Yield opportunity clustering via embeddings  

---

## 📄 License

MIT License — free to modify and extend for your own research or bots.

---

## 💡 About DeepBlockAI

DeepBlockAI is an emerging suite of autonomous crypto intelligence bots built to provide actionable alpha across DeFi, trading, and yield ecosystems.

Designed for:

- Traders  
- Analysts  
- Automation builders  
- Yield optimizers  
- Infra and bot developers  

---

**Made with 🔥 by DeepBlockAI**
