import streamlit as st
import pandas as pd

st.set_page_config(page_title="Audit AI Dashboard", layout="centered")
st.title("🧾 AI-Powered Audit & Engagement Dashboard")

st.markdown("Upload the latest **Balance Sheet** and **Profit & Loss Statement** in Excel format (.xlsx).")

bs_file = st.file_uploader("📂 Upload Balance Sheet", type=["xlsx"])
pl_file = st.file_uploader("📂 Upload Profit & Loss", type=["xlsx"])

def get_value(df, key):
    try:
        return df[df['Particulars'].str.strip().str.lower() == key.strip().lower()]['Amount'].values[0]
    except IndexError:
        st.error(f"❌ '{key}' not found. Check spelling or formatting.")
        return None

if bs_file and pl_file:
    bs_df = pd.read_excel(bs_file)
    pl_df = pd.read_excel(pl_file)

    st.subheader("🧮 Balance Sheet Preview")
    st.write(bs_df)

    st.subheader("📊 Profit & Loss Preview")
    st.write(pl_df)

    # Extract values
    current_assets = get_value(bs_df, "Current Assets")
    current_liabilities = get_value(bs_df, "Current Liabilities")
    total_liabilities = get_value(bs_df, "Total Liabilities")
    reserves = get_value(bs_df, "Reserves and Surplus")
    share_capital = get_value(bs_df, "Share Capital")
    total_assets = get_value(bs_df, "Total Assets")

    revenue = get_value(pl_df, "Revenue from Operations")
    gross_profit = get_value(pl_df, "Gross Profit")
    net_profit = get_value(pl_df, "Net Profit")
    interest_expense = get_value(pl_df, "Interest Expense")

    if None in [current_assets, current_liabilities, total_liabilities, reserves, share_capital, total_assets,
                revenue, gross_profit, net_profit, interest_expense]:
        st.warning("⚠️ Missing data found. Please upload files in correct format.")
        st.stop()

    # Calculate Ratios
    current_ratio = round(current_assets / current_liabilities, 2) if current_liabilities else None
    debt_equity_ratio = round(total_liabilities / (share_capital + reserves), 2)
    gp_margin = round(gross_profit / revenue, 2)
    np_margin = round(net_profit / revenue, 2)
    roa = round(net_profit / total_assets, 2)
    interest_coverage = round(net_profit / interest_expense, 2) if interest_expense else None

    # Show Ratios
    st.subheader("📌 Tax Audit Ratios")
    ratios = {
        "Current Ratio": current_ratio,
        "Debt-to-Equity Ratio": debt_equity_ratio,
        "Gross Profit Margin": gp_margin,
        "Net Profit Margin": np_margin,
        "Return on Assets": roa,
        "Interest Coverage Ratio": interest_coverage
    }
    st.table(pd.DataFrame(ratios.items(), columns=["Ratio", "Value"]))

    # Decision Logic
    decision = "✅ Accept/Continue Engagement"
    if current_ratio < 1 or interest_coverage < 1.5 or np_margin < 0.05:
        decision = "⚠️ High Risk – Consider Not Accepting/Continuing Engagement"

    st.subheader("📌 Final Decision")
    st.success(decision)

    # PDF Download (Optional)
    with st.expander("📥 Export & Share"):
        import io
        from fpdf import FPDF

        buffer = io.BytesIO()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Audit AI Dashboard - Summary", ln=1, align="C")

        for k, v in ratios.items():
            pdf.cell(200, 10, txt=f"{k}: {v}", ln=1)

        pdf.cell(200, 10, txt=f"Final Decision: {decision}", ln=1)
        pdf.output(buffer)
        st.download_button("📄 Download PDF Summary", buffer.getvalue(), file_name="Audit_Report.pdf")

        st.text("To share with team, simply send the downloaded PDF.")

else:
    st.info("⬆️ Please upload both Balance Sheet and Profit & Loss files.")

