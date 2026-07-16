import streamlit as st
from ratios import get_all_ratios

st.title("Financial Ratio Dashboard")

ticker_symbol = st.text_input("Enter a ticker symbol", "AAPL")

if ticker_symbol:
    ratios = get_all_ratios(ticker_symbol)

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Ratio", round(ratios["current_ratio"], 2) if ratios["current_ratio"] else "N/A")
    col2.metric("Debt to Equity (yfinance)", round(ratios["debt_to_equity_yf"], 2) if ratios["debt_to_equity_yf"] else "N/A")
    col3.metric("Net Margin (yfinance)", f"{round(ratios['net_margin_yf'] * 100, 1)}%" if ratios["net_margin_yf"] else "N/A")

    st.subheader("From SEC EDGAR")
    col4, col5, col6 = st.columns(3)
    col4.metric("Debt to Equity", round(ratios["debt_to_equity_edgar"], 2) if ratios["debt_to_equity_edgar"] else "N/A")
    col5.metric("Net Margin", f"{round(ratios['net_margin_edgar'] * 100, 1)}%" if ratios["net_margin_edgar"] else "N/A")
    col6.metric("Return on Equity", f"{round(ratios['roe_edgar'] * 100, 1)}%" if ratios["roe_edgar"] else "N/A")