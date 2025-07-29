import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fixed Income Risk Dashboard", layout="wide")

# Load data
pnl_df = pd.read_excel("powerbi_dashboard_data.xlsx")
dv01_df = pd.read_excel("powerbi_dv01_data.xlsx")

# Sidebar
st.sidebar.title("📊 Dashboard Filters")
date_range = st.sidebar.date_input("Select date range", [pnl_df["Date"].min(), pnl_df["Date"].max()])

# Confidence level selector for VaR
confidence_level = st.sidebar.slider("Select Confidence Level for VaR (%)", min_value=90, max_value=99, value=95)

# Filter data by date
pnl_df = pnl_df[(pnl_df["Date"] >= pd.to_datetime(date_range[0])) & (pnl_df["Date"] <= pd.to_datetime(date_range[1]))]

# Summary cards
total_dv01 = dv01_df["DV01 ($)"].sum()
var_percentile = 100 - confidence_level
var_dynamic = np.percentile(pnl_df["Total_PnL"], var_percentile)

col1, col2 = st.columns(2)
col1.metric(f"📉 {confidence_level}% Historical VaR", f"${var_dynamic:,.2f}")
col2.metric("📐 Total DV01", f"${total_dv01:,.2f}")

# DV01 bar chart
st.subheader("📐 DV01 Exposure by Tenor")
st.bar_chart(dv01_df.set_index("Tenor")["DV01 ($)"])

# PnL Line Chart
st.subheader("📈 Daily PnL by Tenor")
tenors = [col for col in pnl_df.columns if col.startswith("PnL_") and col != "Total_PnL"]
st.line_chart(pnl_df.set_index("Date")[tenors + ["Total_PnL"]])

# PnL Distribution
st.subheader("📊 Distribution of Total Daily PnL")
fig, ax = plt.subplots()
sns.histplot(pnl_df["Total_PnL"], bins=40, kde=True, ax=ax)
ax.axvline(var_dynamic, color="red", linestyle="--", label=f"{confidence_level}% VaR = ${var_dynamic:.2f}M")
ax.legend()
ax.set_xlabel("Total Daily PnL ($)")
ax.set_title("Distribution of Daily Portfolio PnL")
st.pyplot(fig)

# Raw Data Toggle
with st.expander("🔍 View Raw Data"):
    st.write("PnL Data:")
    st.dataframe(pnl_df)
    st.write("DV01 Exposure:")
    st.dataframe(dv01_df)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        Made with ❤️ by <b>Mudit</b><br>
        Fixed Income Risk & Performance Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
