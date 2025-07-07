
import streamlit as st
from datetime import datetime
from pnsea import NSE

nse = NSE()

SYMBOLS = ["NIFTY", "BANKNIFTY"]

def detect_trend(pcr):
    if pcr is None:
        return "Neutral", "-"
    if pcr > 1.3:
        return "📈 Bullish", "High PCR"
    elif pcr < 0.7:
        return "🔴 Bearish", "Low PCR"
    else:
        return "⚖️ Neutral", "Balanced PCR"

def fetch_insights(symbol):
    expiries = nse.options.expiry_dates(symbol)
    if not expiries:
        return None
    expiry = expiries[0]
    chain = nse.options.option_chain(symbol, expiry_date=expiry)

    if chain.empty:
        return None

    pe_oi = chain[chain['type'] == 'PE'][['strikePrice', 'openInterest']].sort_values(by='openInterest', ascending=False)
    ce_oi = chain[chain['type'] == 'CE'][['strikePrice', 'openInterest']].sort_values(by='openInterest', ascending=False)

    max_put_strike = pe_oi.iloc[0]['strikePrice']
    max_call_strike = ce_oi.iloc[0]['strikePrice']
    max_put_oi = pe_oi.iloc[0]['openInterest']
    max_call_oi = ce_oi.iloc[0]['openInterest']

    total_pe_oi = pe_oi['openInterest'].sum()
    total_ce_oi = ce_oi['openInterest'].sum()
    pcr = total_pe_oi / total_ce_oi if total_ce_oi else None

    trend, reason = detect_trend(pcr)
    suggested_trade = f"Buy {int(max_call_strike)}CE" if trend == "📈 Bullish" else (
                      f"Buy {int(max_put_strike)}PE" if trend == "🔴 Bearish" else "Wait")

    return {
        "symbol": symbol,
        "pcr": round(pcr, 2) if pcr else "-",
        "trend": trend,
        "reason": reason,
        "max_pe_strike": int(max_put_strike),
        "max_ce_strike": int(max_call_strike),
        "suggested_trade": suggested_trade,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

st.set_page_config(page_title="FS Traders Official - Market Calls", layout="wide")
st.title("📊 FS Traders Official - Live Market Research Dashboard")

for symbol in SYMBOLS:
    insights = fetch_insights(symbol)
    if insights:
        with st.container():
            st.subheader(f"📈 {symbol}")
            st.markdown(f"**Trend:** {insights['trend']}")
            st.markdown(f"**PCR:** {insights['pcr']} — {insights['reason']}")
            st.markdown(f"**Highest PE OI at:** {insights['max_pe_strike']} | **Highest CE OI at:** {insights['max_ce_strike']}")
            st.markdown(f"**Suggested Trade:** `{insights['suggested_trade']}`")
            st.caption(f"Last updated: {insights['timestamp']}")
    else:
        st.warning(f"No data available for {symbol}")
