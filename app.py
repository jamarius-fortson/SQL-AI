import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
from sqlalchemy import create_engine, text
from config import config
from agent import SQLQueryAgent
from visualizer import ResultVisualizer
from setup_db import create_sample_database

# Performance & Layout
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="💎",
    layout="wide",
)

# Premium UI Styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');

    :root {{
        --accent: #00e5ff;
        --accent-glow: rgba(0, 229, 255, 0.3);
        --bg: #05070a;
        --card: #0d1117;
    }}

    .stApp {{
        background: radial-gradient(circle at 50% -20%, #112244 0%, var(--bg) 80%);
        font-family: 'Outfit', sans-serif;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(13, 17, 23, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }}

    h1, h2, h3 {{
        background: linear-gradient(120deg, #fff 0%, #7dd3fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.03em;
    }}

    .metric-card {{
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}

    .stButton > button {{
        background: linear-gradient(135deg, #0062ff 0%, #00e5ff 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.3s ease !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 20px var(--accent-glow);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px;
        background-color: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: rgba(255,255,255,0.02);
        border-radius: 8px 8px 0 0;
        padding: 0 20px;
        color: #94a3b8;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: rgba(0, 229, 255, 0.1) !important;
        color: var(--accent) !important;
        border-bottom: 2px solid var(--accent) !important;
    }}

    code {{
        font-family: 'Fira Code', monospace !important;
    }}
</style>
""", unsafe_allow_html=True)

# Database Architecture
if config.DATABASE_TYPE == "sqlite" and not os.path.exists(config.SQLITE_DB_PATH):
    with st.status("🏗️ Generating Synthetic Ecosystem...", expanded=True):
        create_sample_database(config.SQLITE_DB_PATH)

# Core Intelligence Engine
@st.cache_resource
def load_engine():
    return SQLQueryAgent(config.DATABASE_URI)

try:
    analyst = load_engine()
except Exception as e:
    st.error(f"Critical Core Failure: {e}")
    st.stop()

# --- SIDEBAR: Operational Command ---
with st.sidebar:
    st.markdown("### 💠 Daniel Command")
    st.caption(f"v{config.APP_VERSION} | Enterprise Edition")
    st.markdown("---")

    st.markdown("### 🔍 Semantic Presets")
    prompts = {
        "📊 Revenue Dynamics": "Analyze revenue trends over the last 12 months with month-over-month growth.",
        "👥 Top Tier Consumers": "Identify the top 10 customers by enterprise value (total spend).",
        "📦 Stock Intelligence": "Which product categories are performing best vs. inventory levels?",
        "🌍 Global Reach": "Breakdown revenue by geographic region and country."
    }
    
    for label, cmd in prompts.items():
        if st.button(label, use_container_width=True):
            st.session_state.prompt = cmd

    st.markdown("---")
    st.markdown("### ⚡ System Telemetry")
    st.success(f"Mode: {config.DATABASE_TYPE.upper()}")
    st.info("LLM: DeepSeek-V3 Enhanced")
    st.info("Safety Level: FAANG Grade")

# --- MAIN: Intelligence Hub ---
header_left, header_right = st.columns([0.7, 0.3])
with header_left:
    st.title("💎 Daniel Analytics")
    st.markdown("#### The Nexus of Natural Language & Structural Intelligence")

with header_right:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT ENGINE", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

# Input interface
with st.container():
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    user_input = st.text_area(
        "Semantic Query Objective",
        value=st.session_state.prompt,
        placeholder="e.g., 'Compare the average order value between repeat and one-time customers'...",
        height=120,
        help="Input your query in natural English. Daniel will handle the SQL translation and logic."
    )
    
    col_x, col_y, _ = st.columns([0.2, 0.2, 0.6])
    with col_x:
        execute = st.button("🚀 EXECUTE", use_container_width=True, type="primary")
    with col_y:
        if st.button("🧹 SCRUB", use_container_width=True):
            st.session_state.prompt = ""
            st.rerun()

if execute and user_input:
    with st.spinner("🤖 Daniel Agent Orchestrating Data..."):
        response = analyst.query(user_input)
        
        if response["success"]:
            # Logic to extract the last executed SQL for visualization
            sql_used = ""
            for action, obs in reversed(response["steps"]):
                if hasattr(action, 'tool_input'):
                    t_input = action.tool_input
                    if isinstance(t_input, dict) and 'query' in t_input:
                        sql_used = t_input['query']
                        break
                    elif isinstance(t_input, str) and "SELECT" in t_input.upper():
                        sql_used = t_input
                        break
            
            # Application Tabs
            tab_viz, tab_data, tab_schema, tab_logic = st.tabs([
                "📊 ANALYTICS DASHBOARD", 
                "📋 RAW DATASET", 
                "🗺️ SCHEMA EXPLORER",
                "🧠 NEURAL REASONING"
            ])

            with tab_viz:
                st.markdown("### 💡 Strategic Insight")
                st.info(response["answer"])
                
                if sql_used:
                    try:
                        engine = create_engine(config.DATABASE_URI)
                        with engine.connect() as conn:
                            df = pd.read_sql(text(sql_used), conn)
                            
                        if not df.empty:
                            m_col1, m_col2 = st.columns([0.7, 0.3])
                            with m_col1:
                                fig = ResultVisualizer.auto_visualize(df, title="Dynamic Visual Intel")
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True)
                            with m_col2:
                                st.markdown("#### Stats Breakdown")
                                st.code(ResultVisualizer.get_summary_stats(df), language="text")
                    except Exception as ve:
                        st.caption(f"Viz Layer Info: {ve}")

            with tab_data:
                if 'df' in locals() and not df.empty:
                    header_d1, header_d2 = st.columns([0.8, 0.2])
                    header_d1.markdown("### 📥 Underlying Assets")
                    
                    # Excel Export logic
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Daniel_Export')
                    
                    header_d2.download_button(
                        label="📥 EXPORT EXCEL",
                        data=output.getvalue(),
                        file_name=f"daniel_intel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                    st.dataframe(df, use_container_width=True, height=500)
                else:
                    st.warning("No structured data frames yielded from this reasoning path.")

            with tab_schema:
                st.markdown("### 🗺️ Database Landscape")
                st.code(analyst.get_schema(), language="sql")

            with tab_logic:
                st.markdown("### ⛓️ Strategic Reasoning Chain")
                for i, (action, observation) in enumerate(response["steps"]):
                    with st.expander(f"Phased Action {i+1}", expanded=(i == len(response["steps"])-1)):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**Action taken:**")
                            st.code(str(action))
                        with c2:
                            st.markdown("**System Observation:**")
                            st.code(observation[:1000] + "..." if len(observation) > 1000 else observation)

        else:
            st.error(f"⚠️ Intelligent Analysis Interrupted: {response['error']}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 2rem; color: #64748b;">
        <p><b>DANIEL DATA INTELLIGENCE</b> • Enterprise Semantic Infrastructure</p>
        <p style="font-size: 0.8rem;">Engineered for mission-critical data decisions. Restricted Access Protocol.</p>
    </div>
""", unsafe_allow_html=True)
