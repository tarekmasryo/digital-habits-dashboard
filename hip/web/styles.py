from __future__ import annotations

import streamlit as st

GLOBAL_CSS = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: transparent;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 45px 0 rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(25px);
        border-radius: 30px;
        padding: 50px;
        margin: 30px 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
        animation: pulse 3s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 15px;
        font-weight: 400;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(15px);
        border-radius: 18px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: scale(1.05);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    .metric-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: inline-block;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 10px 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .metric-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .metric-change {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 8px;
    }

    .insight-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #10b981;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        animation: slideInLeft 0.6s ease-out;
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .insight-warning {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(239, 68, 68, 0.15) 100%);
    }

    .insight-danger {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
    }

    .insight-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .insight-text {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }

    .section-header {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 20px 30px;
        margin: 30px 0 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .section-icon {
        font-size: 2rem;
        animation: rotate 3s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }

    .section-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.7);
        margin: 5px 0 0 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 35px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        padding: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        font-size: 1.02rem;
        padding: 14px 32px;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(
            135deg,
            rgba(102, 126, 234, 0.3) 0%,
            rgba(118, 75, 162, 0.3) 100%
        );
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    [data-testid="stSidebar"] .element-container {
        color: white;
    }

    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    .loading {
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.1) 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }

    .status-badge {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }

    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }

    .status-danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }

    .tooltip-custom {
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 10px;
        color: white;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>"""

DISABLE_ANIMATIONS_CSS = """<style>
* { animation: none !important; transition: none !important; }
</style>"""


def apply_global_styles(disable_animations: bool = False) -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    if disable_animations:
        st.markdown(DISABLE_ANIMATIONS_CSS, unsafe_allow_html=True)
