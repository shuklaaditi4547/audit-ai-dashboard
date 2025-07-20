import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Audit Automation Dashboard", layout="centered")

st.title("🧾 AI Audit Automation - Engagement Dashboard")

st.markdown("Upload your **Balance Sheet** and **P&L** Excel files to begin.")

bs_file = st.file_uploader("📂 Upload Balance Sheet (Excel)", type=["xlsx"], key="bs")
pl_file = st.file_uploader("📂 Upload Profit & Loss Statement (Excel)", type=["xlsx"], key="pl")

def calculate_ratios(bs_df, pl_df):
    try:
        current_assets = bs_df.loc[bs_df['Particulars'].str.contains("Current Assets", case=False), 'Amount'].values[0]
        current_liabilities = bs_df.loc[bs_df['Particulars'].str.contains("Current Liabilities", case=False), 'Amount'].values[0]
        total_liabilities = bs_df.loc[bs_df['Particulars'].str.contains("Total Liabilities", case=False), 'Amount'].values[0]
        total_equity = bs_df.loc[bs_df['Particulars'].str.contains("Equity", case=False), 'Amount'].values[0]
        gross_profit = pl_df.loc[pl_df['Particulars'].str.contains("Gross Profit", case=False), 'Amount'].values[0]
        net_profit = pl_df.loc[pl_df['Particulars'].str.contains("Net Profit", case=False), 'Amount'].values[0]
        revenue = pl_df.loc[pl_df['Particulars'].str.contains("Revenue|Sales", case=False), 'Amount'].values[0]
        interest_expense = pl_df.loc[pl_df['Particulars'].str.contains("Interest", case=False), 'Amount'].values[0]
        total_assets = bs_df.loc[bs_df['Particulars'].str.contains("Total Assets", case=False), 'Amount'].values[0]
        
        ratios = {
            "Current Ratio": current_assets / current_liabilities,
            "Debt-to-Equity Ratio": total_liabilities / total_equity,
            "Gross Profit Margin": (gross_profit / revenue) * 100,
            "Net Profit Margin": (net_profit / revenue) * 100,
            "Return on Assets": (net_profit / total_assets) * 100,
            "Interest Coverage Ratio": net_profit / interest_expense if interest_expense != 0 else "N/A"
        }
        return ratios
    except Exception as e:
        st.error(f"Error calculating ratios: {e}")
        return {}

if bs_file and pl_file:
    bs_df = pd.read_excel(bs_file)
    pl_df = pd.read_excel(pl_file)

    st.success("Files uploaded successfully!")

    ratios = calculate_ratios(bs_df, pl_df)

    if ratios:
        st.subheader("📊 Calculated Tax Audit Ratios")
        for key, value in ratios.items():
            st.write(f"**{key}**: {round(value, 2) if isinstance(value, float) else value}")

        st.subheader("🔍 Audit Comment & Engagement Decision")

        if ratios["Current Ratio"] < 1:
            st.error("⚠️ Poor liquidity position detected. Engagement Risk: HIGH")
        elif ratios["Net Profit Margin"] < 5:
            st.warning("⚠️ Low profitability. Proceed with caution.")
        else:
            st.success("✅ Financial position appears stable. Engagement Risk: LOW")

        st.markdown("---")
        st.download_button("📥 Download Report", data=str(ratios), file_name="audit_report.txt")
