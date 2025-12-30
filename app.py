import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Forensic Financial Dashboard",
    layout="wide"
)

# ---------------- Styling ----------------
st.markdown("""
<style>
body {
    background-color: #0b1c2d;
    color: white;
}
[data-testid="stMetric"] {
    background-color: #13293d;
    padding: 18px;
    border-radius: 14px;
}
[data-testid="stMetricLabel"] {
    color: #9fbcd9;
}
[data-testid="stMetricValue"] {
    color: white;
    font-size: 28px;
}
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Forensic Financial Health Dashboard")
st.caption("Piotroski F-Score • Montier C-Score • Ohlson O-Score")

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader(
    "Upload financial data (Excel)",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # ---------------- Company Selector ----------------
    company = st.selectbox("Select Company", df["Company"].unique())
    df_c = df[df["Company"] == company].sort_values("Year").copy()

    df_c["Year"] = df_c["Year"].astype(str)
    latest = df_c.iloc[-1]

    # ---------------- Scores ----------------
    f_score = latest["F_Score"]
    c_score = latest["C_Score"]
    o_score = latest["O_SCORE"]

    f_label = "Strong" if f_score >= 7 else "Moderate" if f_score >= 4 else "Weak"
    c_label = "Low Risk" if c_score <= 1 else "Moderate Risk" if c_score <= 3 else "High Risk"
    o_label = "Stable" if o_score <= 1 else "At Risk"

    # ---------------- Score Cards ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Piotroski F-Score", f"{int(f_score)} / 9")
        st.caption(f"📌 {f_label}")

    with col2:
        st.metric("Montier C-Score", f"{int(c_score)} / 6")
        st.caption(f"📌 {c_label}")

    with col3:
        st.metric("Ohlson O-Score", round(o_score, 2))
        st.caption(f"📌 {o_label}")

    # ---------------- Overall Interpretation ----------------
    if f_score >= 7 and c_score <= 1 and o_score <= 1:
        overall = "🟢 Financially Healthy"
        color = "#1f7a1f"
    elif c_score >= 4 or o_score >= 3:
        overall = "🔴 High Forensic Risk"
        color = "#7a1f1f"
    else:
        overall = "🟡 Watchlist Company"
        color = "#7a6a1f"

    st.markdown(f"""
    <div style="
        background-color:{color};
        padding:20px;
        border-radius:16px;
        margin-top:20px;
        font-size:22px;
        font-weight:600;
        text-align:center;
    ">
    Overall Interpretation: {overall}
    </div>
    """, unsafe_allow_html=True)

    # ---------------- Accruals Quality Card ----------------
    st.markdown("### 🧮 Earnings Quality (Accrual Analysis)")

    cf_accrual = latest["CF_Accrual_Ratio"]
    bs_accrual = latest["BS_Accrual_Ratio"]
    accrual_zone = latest["Accrual_Zone"]
    accrual_text = latest["Accrual_Interpretation"]

    if accrual_zone == "High-Quality Earnings":
        bg_color = "#1f7a1f"
    elif accrual_zone == "Early Warning Zone":
        bg_color = "#7a6a1f"
    elif accrual_zone == "Asset-Heavy Operations":
        bg_color = "#1f4e7a"
    else:
        bg_color = "#7a1f1f"

    st.markdown(
        f"""
        <div style="
            background-color:{bg_color};
            padding:22px;
            border-radius:18px;
            margin-top:10px;
            color:white;
        ">
            <h3>Accrual Zone: {accrual_zone}</h3>
            <p><b>Cash-Flow Accrual Ratio:</b> {cf_accrual:.3f}</p>
            <p><b>Balance-Sheet Accrual Ratio:</b> {bs_accrual:.3f}</p>
            <p>📌 {accrual_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Score Trends ----------------
    st.markdown("### 📈 Score Trends")

    fig = px.line(
        df_c,
        x="Year",
        y=["F_Score", "C_Score", "O_SCORE"],
        markers=True,
        title="Forensic Scores Trend Over Time"
    )

    fig.update_layout(
        plot_bgcolor="#0b1c2d",
        paper_bgcolor="#0b1c2d",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"))
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Cash Flow vs Net Income ----------------
    st.markdown("### 💰 Cash Flow vs Net Income")

    fig2 = px.bar(
        df_c,
        x="Year",
        y=["CFO", "Net_Income"],
        barmode="group"
    )

    fig2.update_layout(
        plot_bgcolor="#0b1c2d",
        paper_bgcolor="#0b1c2d",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"))
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("👆 Please upload an Excel file to begin.")
