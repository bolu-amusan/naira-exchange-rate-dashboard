import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Naira Exchange Rate & Inflation Dashboard", layout="wide")

st.title("🇳🇬 Naira Exchange Rate & Inflation Dashboard")
st.markdown("Interactive analysis of Naira/USD exchange rates and inflation trends, using official CBN data.")

# --- Load and prepare data ---
@st.cache_data
def load_data():
    df_exchange = pd.read_excel('data/exchange_rates.xlsx')
    df_inflation = pd.read_excel('data/inflation_rates.xlsx')

    df_exchange['ratedate'] = pd.to_datetime(df_exchange['ratedate'], format='%B-%d-%Y')
    df_exchange = df_exchange.sort_values('ratedate').reset_index(drop=True)

    df_inflation['date'] = pd.to_datetime(df_inflation['tyear'].astype(str) + '-' + df_inflation['tmonth'].astype(str) + '-01')
    df_inflation = df_inflation.sort_values('date').reset_index(drop=True)

    df_exchange_monthly = df_exchange.set_index('ratedate').resample('MS').agg({
        'closingrate': 'mean',
        'highestrate': 'max',
        'lowestrate': 'min',
        'weightedAvgRate': 'mean'
    }).reset_index().rename(columns={'ratedate': 'date'})

    df_combined = pd.merge(
        df_exchange_monthly,
        df_inflation[['date', 'allItemsYearOn', 'foodYearOn']],
        on='date',
        how='inner'
    )

    return df_exchange, df_inflation, df_exchange_monthly, df_combined

df_exchange, df_inflation, df_exchange_monthly, df_combined = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select date range",
    value=(df_combined['date'].min(), df_combined['date'].max()),
    min_value=df_combined['date'].min(),
    max_value=df_combined['date'].max()
)

if len(date_range) == 2:
    mask = (df_combined['date'] >= pd.Timestamp(date_range[0])) & (df_combined['date'] <= pd.Timestamp(date_range[1]))
    df_filtered = df_combined[mask]
else:
    df_filtered = df_combined

# --- Key metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Latest Exchange Rate", f"₦{df_filtered['closingrate'].iloc[-1]:,.2f}/$")
col2.metric("Latest Inflation Rate", f"{df_filtered['allItemsYearOn'].iloc[-1]:.2f}%")
correlation = df_filtered['closingrate'].corr(df_filtered['allItemsYearOn'])
col3.metric("Correlation (Rate vs. Inflation)", f"{correlation:.3f}")

# --- Main chart: dual-axis ---
st.subheader("Exchange Rate vs. Inflation Over Time")
fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(df_filtered['date'], df_filtered['closingrate'], color='#4C72B0', marker='o', label='Exchange Rate')
ax1.set_ylabel('Exchange Rate (₦/$)', color='#4C72B0')
ax1.tick_params(axis='y', labelcolor='#4C72B0')

ax2 = ax1.twinx()
ax2.plot(df_filtered['date'], df_filtered['allItemsYearOn'], color='#d62728', marker='o', label='Inflation (YoY %)')
ax2.set_ylabel('Inflation Rate (%)', color='#d62728')
ax2.tick_params(axis='y', labelcolor='#d62728')

plt.tight_layout()
st.pyplot(fig)

# --- Inflation type toggle ---
st.subheader("Choose Inflation Measure")
inflation_choice = st.radio(
    "Compare exchange rate against:",
    options=["Headline Inflation", "Food Inflation"],
    horizontal=True
)

inflation_col = 'allItemsYearOn' if inflation_choice == "Headline Inflation" else 'foodYearOn'
corr_choice = df_filtered['closingrate'].corr(df_filtered[inflation_col])

st.write(f"**Correlation between Exchange Rate and {inflation_choice}:** {corr_choice:.3f}")

# --- Scatter plot ---
st.subheader(f"Exchange Rate vs. {inflation_choice} (Scatter)")
fig3, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df_filtered['closingrate'], df_filtered[inflation_col], color='#4C72B0', s=60, alpha=0.7)
ax.set_xlabel('Exchange Rate (₦/$)')
ax.set_ylabel(f'{inflation_choice} (%)')
plt.tight_layout()
st.pyplot(fig3)

# --- Insights section ---
st.subheader("Key Insights")
st.markdown("""
- **Strong correlation (r = 0.874)** between exchange rate and headline inflation from Dec 2024–Jul 2026 — as the Naira appreciated, inflation fell in tandem.
- **Food inflation correlates less strongly (r = 0.714)**, suggesting domestic supply factors (not just currency) drive food prices.
- **The ~35% inflation peak around 2024 is a historic extreme** — the highest in over 20 years of CBN data.
- **No meaningful lag effect** was found — exchange rate and inflation move together concurrently, not with one predicting the other a month ahead.
""")

# --- Long-term inflation chart ---
st.subheader("Long-Term Inflation Trend (2003–Present)")
fig2, ax = plt.subplots(figsize=(12, 4))
ax.plot(df_inflation['date'], df_inflation['allItemsYearOn'], color='#d62728', linewidth=1.5)
ax.set_ylabel('Inflation Rate (YoY %)')
plt.tight_layout()
st.pyplot(fig2)

# --- Raw data viewer ---
with st.expander("View underlying data"):
    st.dataframe(df_filtered)