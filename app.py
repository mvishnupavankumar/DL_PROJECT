import streamlit as st

from live_monitoring import render_live_monitoring

st.set_page_config(
    page_title="AegisOps — Live Monitoring",
    page_icon="🛠️",
    layout="wide",
)

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1250px;}
.agent-card {padding: 14px 16px; border: 1px solid #d8dee9; border-radius: 12px; margin-bottom: 10px;}
.small {font-size: 0.88rem; opacity: 0.8;}
</style>
""", unsafe_allow_html=True)

st.title("🛠️ AegisOps — Live Monitoring")
st.caption(
    "Live host and local-service telemetry, LSTM anomaly detection, "
    "multi-agent investigation, approval-gated remediation, and recovery verification."
)

render_live_monitoring()
