
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Dashboard Financeiro B3", layout="wide")
st.title("📈 Dashboard Fundamentalista - B3 (com DY do Fundamentus)")

empresas = {
    "PETR4": "PETR4.SA", "ELET3": "ELET3.SA", "PRIO3": "PRIO3.SA", "RAIZ4": "RAIZ4.SA", "RRRP3": "RRRP3.SA",
    "VALE3": "VALE3.SA", "CSNA3": "CSNA3.SA", "GGBR4": "GGBR4.SA", "USIM5": "USIM5.SA", "CMIN3": "CMIN3.SA",
    "ITUB4": "ITUB4.SA", "BBDC4": "BBDC4.SA", "BBAS3": "BBAS3.SA", "SANB11": "SANB11.SA", "BPAC11": "BPAC11.SA",
    "MGLU3": "MGLU3.SA", "LREN3": "LREN3.SA", "AMER3": "AMER3.SA", "ARZZ3": "ARZZ3.SA", "VIIA3": "VIIA3.SA",
    "JBSS3": "JBSS3.SA", "BRFS3": "BRFS3.SA", "MRFG3": "MRFG3.SA", "RAIL3": "RAIL3.SA", "ABEV3": "ABEV3.SA"
}

def get_dividend_yield_fundamentus(ticker):
    try:
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        td_list = soup.find_all("td")
        for i, td in enumerate(td_list):
            if "Div. Yield" in td.text:
                valor = td_list[i+1].text.strip().replace("%", "").replace(",", ".")
                return float(valor)
    except:
        return None

st.sidebar.header("Seleção de Ações")
selecionadas = st.sidebar.multiselect("Escolha até 5 ações para análise:", list(empresas.keys()), default=["PETR4", "VALE3", "ITUB4"])

df_indicadores = []

for acao in selecionadas:
    ticker = yf.Ticker(empresas[acao])
    info = ticker.info
    dy = get_dividend_yield_fundamentus(acao)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"{acao} - P/L", round(info.get("trailingPE", 0), 2))
    col2.metric("ROE", f"{round(info.get('returnOnEquity', 0)*100, 2)}%")
    col3.metric("Margem Líquida", f"{round(info.get('netMargins', 0)*100, 2)}%")
    col4.metric("Dividend Yield", f"{dy}%" if dy else "N/A")
    st.markdown("---")

    df_indicadores.append({
        "Ação": acao,
        "P/L": info.get("trailingPE", 0),
        "ROE (%)": info.get("returnOnEquity", 0) * 100,
        "Margem Líquida (%)": info.get("netMargins", 0) * 100,
        "Dividend Yield (%)": dy if dy else 0
    })

if df_indicadores:
    df_plot = pd.DataFrame(df_indicadores)
    fig = px.bar(df_plot, x="Ação", y=["P/L", "ROE (%)", "Margem Líquida (%)", "Dividend Yield (%)"],
                 barmode="group", title="Indicadores Comparativos")
    st.plotly_chart(fig, use_container_width=True)
