import streamlit as st
from datetime import datetime
from pnsea import NSE

nse = NSE()

SYMBOLS = ["NIFTY", "BANKNIFTY"]

def detect_trend(pcr):
    if pcr is None:
        return "⚖️ Neutral", "-"
    if pcr > 1.3:
        return "📈 Bullish", "High PCR"
    elif pcr < 0.7:
        return "🔴 Bearish", "Low PCR"
    else:
        return "⚖️ Neutral", "Balanced PCR"

def fetch_insights(symbol):
    try:
        expiries = nse.options.expiry_dates(symbol)
        if not expiries:
            return None

        expiry = expiries[0]
        chain = nse.options.option_chain(symbol, expiry_date=expiry)

        if chain is None or not hasattr(chain, 'empty') or chain.empty:
            return None

        pe_oi = chain[chain['type'] == 'PE'][['strikePrice', 'openInterest']].sort_values(by='openInterest', ascending=False)
        ce_oi = chain[chain['type'] == 'CE'][['strikePrice', 'openInterest']].sort_values(by='openInterest', ascending=False)

        max_put_strike = pe_oi.iloc[0]['strikePrice']
        max_call_strike = ce_oi.iloc[0]['strikePrice']

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

    except Exception as e:
        print(f"⚠️ Error fetching insights for {symbol}: {e}")
        return None

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="FS Traders Official - Market Calls", layout="wide")
st.title("📊 FS Traders Official - Live Market Research Dashboard")

st.markdown("##### Powered by Real-Time NSE Option Chain Analysis")

for symbol in SYMBOLS:
    insights = fetch_insights(symbol)
    st.divider()
    if insights:
        st.subheader(f"📈 {symbol} - Trend: {insights['trend']}")
        st.metric(label="📉 PCR", value=insights['pcr'], delta=insights['reason'])
        st.markdown(f"🔵 **Highest PE OI at:** `{insights['max_pe_strike']}`")
        st.markdown(f"🔴 **Highest CE OI at:** `{insights['max_ce_strike']}`")
        st.markdown(f"📢 **Suggested Trade:** `{insights['suggested_trade']}`")
        st.caption(f"Last updated: {insights['timestamp']}")
    else:
        st.error(f"❌ No data available for {symbol}. NSE may be blocking Streamlit Cloud.")
