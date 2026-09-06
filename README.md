# Naira Exchange Rate & Inflation Dashboard

An interactive Streamlit dashboard analyzing the relationship between Naira/USD exchange rates and inflation, using official data from the Central Bank of Nigeria (CBN).

## Overview
This project explores whether — and how — Naira exchange rate movements relate to inflation trends in Nigeria, using real government data. It combines two official CBN datasets, resolves a frequency mismatch between them (daily vs. monthly data), and presents the findings through an interactive Streamlit dashboard.

## Tech Stack
- Python (pandas)
- Streamlit
- Matplotlib / Seaborn
- Data source: Central Bank of Nigeria (cbn.gov.ng)

## Data Sources
Both datasets were manually exported from CBN's official rates pages (they render dynamically via JavaScript, so direct download via their "Export to Excel" feature was required — see `data/README.md` for details):

- **Exchange Rate** (`data/exchange_rates.xlsx`): Daily Naira/USD rates, December 2, 2024 – September 4, 2026 (440 daily records)
- **Inflation Rate** (`data/inflation_rates.xlsx`): Monthly inflation figures, January 2003 – July 2026 (283 monthly records)

## Project Structure
├── data/ # source Excel files + data source documentation
├── notebooks/ # data exploration and cleaning
├── images/ # exported charts
└── README.md


## Approach & Key Decisions

**1. Data quality investigation.** The exchange rate file includes deal/turnover columns (`noOfDeals`, `noOfDeals_InterBank`, etc.) that are only populated from March 2026 onward — CBN appears to have started tracking these specific metrics at that point. Core rate columns (`closingrate`, `highestrate`, `lowestrate`, `weightedAvgRate`, `simpleAvgRate`) are populated for the full range back to December 2024. This project uses the full range for core rate analysis, and notes the shorter window explicitly wherever turnover/deal metrics are involved.

**2. Frequency mismatch: daily vs. monthly.** Exchange rate data is recorded daily; inflation is only reported monthly. To compare them meaningfully, exchange rate data was resampled to monthly frequency — using **mean** for closing/weighted average rates (a representative "typical" monthly rate) and **max/min** for highest/lowest rates (preserving the actual extremes reached within each month, rather than averaging them away).

**3. Date range overlap.** The two datasets only overlap from December 2024 to July 2026 (limited by inflation data's most recent report). An inner join on the monthly date produces a clean combined dataset for direct comparison, while the exchange rate's full range (through September 2026) is still used separately for a longer-term rate-only view.

## Key Findings

**1. Strong correlation between exchange rate and inflation (r = 0.874).** Over Dec 2024–Jul 2026, as the Naira appreciated (exchange rate falling from ~₦1600 to ~₦1360/$), headline inflation fell sharply in tandem (from ~35% to ~15%). Both series moved in the same direction throughout this window.

**2. Food inflation correlates less strongly (r = 0.714) than headline inflation.** This is somewhat counterintuitive — food is often assumed to be highly import-sensitive — and suggests food prices are also shaped by domestic factors (agricultural supply, insecurity in farming regions, seasonal harvests) independent of currency movements.

**3. Current inflation episode is a historic extreme.** Viewed against 23 years of data (2003–2026), the ~35% peak around 2024 is the highest inflation rate in the dataset, exceeding even the 2016-2017 recession-era spike (~18-19%). The subsequent decline to ~15% by mid-2026 represents a rapid improvement from a historic high, though still elevated by long-term historical standards.

**4. No meaningful lag effect found.** Testing whether the previous month's exchange rate predicts the current month's inflation produced a nearly identical correlation (0.867) to the same-month comparison (0.874) — suggesting the two series move concurrently rather than one clearly leading the other.

**Overall narrative:** Nigeria's inflation and exchange rate have moved closely together through a historic inflation episode and subsequent recovery, though the relationship is more nuanced for food prices specifically, and the data doesn't support claiming exchange rate changes predict inflation with a time lag — they appear to move together in real time.

**Caveat:** A strong correlation over one continuous declining trend (as seen here) should be interpreted cautiously — it doesn't establish causation, and a longer window with independent up/down cycles would give more confidence in the strength of this relationship.

## Dashboard
*(To be added — Streamlit app link/instructions)*

## Setup / How to Run
1. Clone this repo
2. Download the datasets from CBN (see `data/README.md`) and place them in `data/`
3. Install dependencies: `pip install pandas matplotlib seaborn streamlit openpyxl`
4. Run the exploration notebook: `notebooks/data_exploration.ipynb`
5. Launch the dashboard: `streamlit run app.py` *(once built)*