# 🔄 Dividend-Fetcher — Live Dividend Tracker CLI

> A terminal dashboard that scrapes the latest declared dividends from Moneycontrol and auto-refreshes them on an interval — handy for spotting upcoming ex-dates while the market is open.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=flat-square)

## ✨ Features

- Parses Moneycontrol's *Dividends Declared* cards (company, type, %, amount, record & ex-dates)
- Auto-refresh loop with console clearing and a timestamped header
- Clean tabular output via `tabulate`
- Graceful handling of network / parsing failures

## 🚀 Usage

```bash
git clone https://github.com/optimus-node-js/Dividend-Fetcher.git
cd Dividend-Fetcher
```

```bash
pip install requests beautifulsoup4 tabulate
python main.py
```

**Part of my dividend toolkit:** [AlgoDividend](https://github.com/optimus-node-js/AlgoDividend) (scraper) · [dividend-fetch-server](https://github.com/optimus-node-js/dividend-fetch-server) (REST API) · [DividendROI-Calculator](https://github.com/optimus-node-js/DividendROI-Calculator) (ROI analysis)

---

## 👤 Author

**Rahul Vishwakarma** — Senior Full Stack Developer · Ahmedabad, India

[![Portfolio](https://img.shields.io/badge/Portfolio-rahul--vishwakarma--portfolio.vercel.app-0A66C2?style=flat-square&logo=vercel&logoColor=white)](https://rahul-vishwakarma-portfolio.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rahul%20Vishwakarma-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/rahul-vishwakarma-101346192)
[![Email](https://img.shields.io/badge/Email-karmarahul67%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:karmarahul67@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-optimus--node--js-181717?style=flat-square&logo=github)](https://github.com/optimus-node-js)

If you find this project useful, consider giving it a ⭐.
