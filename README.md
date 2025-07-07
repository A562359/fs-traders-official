# 📊 FS Traders Official

**FS Traders Official** is an AI-powered web dashboard that generates real-time trend-based trading calls using live F&O data and PCR (Put/Call Ratio) from NSE.

---

## 🚀 Features
- 🔎 Detects market trend using live Option Chain data
- 📈 Calculates PCR, OI build-up and strike activity
- 📩 Suggests BUY/SELL options based on real data
- 🕒 Auto-refresh every 3–5 minutes
- 🌐 Live deployment on Streamlit Cloud

---

## 📦 Files
| File | Description |
|------|-------------|
| `trend_call_dashboard.py` | Streamlit dashboard code |
| `requirements.txt` | Python dependencies |
| `README.md` | This guide |

---

## ⚙️ Run Locally

```bash
pip install -r requirements.txt
streamlit run trend_call_dashboard.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push files to GitHub (repo: `fs-traders-official`)
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click “New App”
   - Repo: `yourusername/fs-traders-official`
   - File: `trend_call_dashboard.py`
4. Click “Deploy”

Your live dashboard will be available at:  
`https://fs-traders-official.streamlit.app`

---

## ✅ Built with ❤️ by FS Traders
