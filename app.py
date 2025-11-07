import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from passlib.context import CryptContext

# ====================
# PAGE CONFIGURATION
# ====================
st.set_page_config(
    page_title="Community Blood Bank",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# PASSWORD HASHING
# ====================
pwd_context = CryptContext(schemes=["sha256_crypt", "bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        st.error(f"Password verification error: {e}")
        return False

def get_password_hash(password):
    """Hash a password using the default scheme"""
    return pwd_context.hash(password)

# ====================
# AGE CALCULATION HELPER
# ====================
def calculate_age(birth_date):
    """Calculate age from date of birth"""
    if birth_date is None:
        return None
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# ====================
# ENHANCED CUSTOM CSS - PROFESSIONAL & POLISHED
# ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* ========================================
   1. GLOBAL & FONT STYLES
   ======================================== */
* {
    font-family: 'Poppins', sans-serif;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main background with subtle gradient */
.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #fff5f5 100%);
}

/* General text visibility */
p, span, div, label {
    color: #1a1a1a;
}

/* Section headers with elegant underline */
h2, h3 {
    color: #b71c1c !important;
    font-weight: 700 !important;
    margin-top: 30px !important;
    margin-bottom: 20px !important;
    position: relative;
    padding-bottom: 12px;
}

h2::after, h3::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, #d32f2f, #ff6b6b);
    border-radius: 2px;
}

h4 {
    color: #2c2c2c !important;
    font-weight: 600 !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Dividers */
hr {
    margin: 30px 0;
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ffcdd2, transparent);
}

/* Enhanced Animations */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.8;
    }
}

.animate-slide {
    animation: slideIn 0.5s ease;
}

/* ========================================
   2. SIDEBAR STYLES
   ======================================== */

/* Sidebar background with gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #b71c1c 0%, #8b1414 100%);
    box-shadow: 4px 0 30px rgba(183, 28, 28, 0.4);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Sidebar text color */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar logo container */
.sidebar-logo {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
}

/* Sidebar navigation buttons - RED BACKGROUND */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%) !important;
    color: white !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 16px;
    font-weight: 600;
    margin: 8px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    text-align: left;
    cursor: pointer;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #e53935 0%, #d32f2f 100%) !important;
    border-color: rgba(255, 255, 255, 0.6) !important;
    transform: translateX(8px) scale(1.02);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(255, 255, 255, 0.3);
}

[data-testid="stSidebar"] .stButton > button:active {
    transform: translateX(6px) scale(1.01);
    background: linear-gradient(135deg, #c62828 0%, #b71c1c 100%) !important;
}

/* ========================================
   3. MAIN LAYOUT & TITLE
   ======================================== */

/* Main content area */
.block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
    animation: fadeInUp 0.6s ease;
}

/* Main title styling with enhanced gradient */
.main-title {
    text-align: center;
    padding: 35px 25px;
    background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 50%, #e53935 100%);
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(183, 28, 28, 0.4);
    margin-bottom: 35px;
    animation: fadeInDown 0.8s ease;
    position: relative;
    overflow: hidden;
}

.main-title::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transform: rotate(45deg);
    animation: pulse 3s infinite;
}

.main-title h1 {
    color: white !important;
    font-size: 46px;
    font-weight: 800;
    margin: 0;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
}

.main-title p {
    color: rgba(255, 255, 255, 0.95);
    font-size: 19px;
    margin-top: 12px;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* Exception for white text on colored backgrounds */
.main-title *, 
[data-testid="stSidebar"] *,
.stButton > button[kind="primary"] * {
    color: white !important;
}

/* ========================================
   4. WIDGETS (Metrics, Tabs, Cards)
   ======================================== */

/* Enhanced Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff 0%, #fff9f9 100%);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(183, 28, 28, 0.12);
    border-left: 5px solid #d32f2f;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle, rgba(211, 47, 47, 0.1), transparent);
    border-radius: 50%;
    transform: translate(30%, -30%);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 35px rgba(183, 28, 28, 0.25);
    border-left-width: 6px;
}

[data-testid="stMetricLabel"] {
    font-size: 16px;
    font-weight: 600;
    color: #2c2c2c;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

[data-testid="stMetricValue"] {
    font-size: 36px;
    font-weight: 800;
    color: #d32f2f;
    line-height: 1.2;
}

[data-testid="stMetricDelta"] {
    font-size: 14px;
    font-weight: 500;
}

/* Enhanced Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: transparent;
    border-bottom: 2px solid #ffcdd2;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    color: #d32f2f;
    border-radius: 12px 12px 0 0;
    padding: 14px 32px;
    font-weight: 600;
    border: 2px solid #ffcdd2;
    border-bottom: none;
    transition: all 0.3s ease;
    position: relative;
}

.stTabs [data-baseweb="tab"]::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: white;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #fff5f5;
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(211, 47, 47, 0.15);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
    color: white !important;
    border-color: #d32f2f;
    box-shadow: 0 6px 15px rgba(211, 47, 47, 0.4);
}

.stTabs [aria-selected="true"]::after {
    background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
}

/* Tab content with smooth transition */
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 25px;
    animation: fadeInUp 0.4s ease;
}

/* Section cards */
.section-card {
    background: linear-gradient(135deg, #ffffff 0%, #fff9f9 100%);
    border-radius: 16px;
    padding: 28px;
    margin: 20px 0;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    border-top: 4px solid #d32f2f;
    transition: all 0.3s ease;
}

.section-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
}

/* ========================================
   5. FORMS & INPUTS
   ======================================== */

/* Labels for all inputs */
.stTextInput > label,
.stSelectbox > label,
.stTextArea > label,
.stNumberInput > label,
.stDateInput > label,
.stCheckbox > label {
    font-weight: 600 !important;
    color: #2c2c2c !important;
    font-size: 15px !important;
    text-align: left !important; 
    width: 100% !important;
    margin-bottom: 8px !important;
}

/* Text, TextArea, Number Input Fields */
.stTextInput > div > div,
.stTextArea > div > div,
.stNumberInput > div > div {
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    background: white !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    color: #1a1a1a !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    background: white !important;
    border: none !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
.stNumberInput input::placeholder {
    color: #999 !important;
    opacity: 1 !important;
    font-weight: 400 !important;
}

/* Select Box */
[data-testid="stSelectbox"] > div > div {
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    background: white !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border: none !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    color: #1a1a1a !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
}

/* Date Input */
[data-testid="stDateInput"] > div > div {
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    background: white !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stDateInput"] input {
    color: #1a1a1a !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    background: white !important;
    border: none !important;
}

/* Enhanced Focus States */
.stTextInput > div > div:focus-within,
.stTextArea > div > div:focus-within,
.stNumberInput > div > div:focus-within,
[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stDateInput"] > div > div:focus-within {
    border-color: #d32f2f !important;
    box-shadow: 0 0 0 4px rgba(211, 47, 47, 0.12), 0 2px 12px rgba(211, 47, 47, 0.15) !important;
    transform: translateY(-1px);
}

/* Auto-fill Fix for Chrome */
input:-webkit-autofill,
input:-webkit-autofill:hover, 
input:-webkit-autofill:focus, 
input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px white inset !important;
    -webkit-text-fill-color: #1a1a1a !important;
}

/* Enhanced Checkbox Styling */
.stCheckbox {
    padding: 8px 0;
}

.stCheckbox > label {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 15px !important;
}

.stCheckbox > label > div[data-testid="stCheckbox"] {
    margin-right: 10px;
}

/* Primary Buttons with enhanced gradient */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 15px 36px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(211, 47, 47, 0.4) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.stButton > button[kind="primary"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.stButton > button[kind="primary"]:hover::before {
    left: 100%;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(211, 47, 47, 0.5) !important;
    background: linear-gradient(135deg, #c62828 0%, #a71a1a 100%) !important;
}

.stButton > button[kind="primary"]:active {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4) !important;
}

/* Secondary Buttons - ALL RED WITH WHITE TEXT */
.stButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]) {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(211, 47, 47, 0.4) !important;
    transition: all 0.3s ease !important;
    cursor: pointer;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):hover {
    background: linear-gradient(135deg, #c62828 0%, #a71a1a 100%) !important;
    color: white !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(211, 47, 47, 0.5) !important;
}

/* Form Submit Buttons */
button[type="submit"] {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 15px 36px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(211, 47, 47, 0.4) !important;
    transition: all 0.3s ease !important;
    cursor: pointer;
}

button[type="submit"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(211, 47, 47, 0.5) !important;
}

/* ========================================
   6. DATA & CHARTS
   ======================================== */

/* DataFrame Container */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    border: 2px solid #ffcdd2 !important;
}

[data-testid="stDataFrame"] > div {
    border: none !important;
    background-color: white !important;
}

/* DataFrame Header */
[data-testid="stHeaderCell"] {
    background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    padding: 12px 16px !important;
}

/* DataFrame Cells */
[data-testid="stDataCell"] {
    background-color: white !important;
    color: #1a1a1a !important;
    border-bottom: 1px solid #f5f5f5 !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
}

/* Alternating row colors */
[data-testid="stDataFrame"] tr:nth-child(even) [data-testid="stDataCell"] {
    background-color: #fafafa !important;
}

[data-testid="stDataFrame"] tr:hover [data-testid="stDataCell"] {
    background-color: #fff5f5 !important;
}

/* Plotly charts container */
.js-plotly-plot {
    border-radius: 16px;
    overflow: hidden;
    background: white;
    padding: 20px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
}

/* Force black text in plotly charts */
.js-plotly-plot .gtitle,
.js-plotly-plot .xtitle,
.js-plotly-plot .ytitle,
.js-plotly-plot .ztitle,
.js-plotly-plot text {
    fill: #1a1a1a !important;
    color: #1a1a1a !important;
    font-family: 'Poppins', sans-serif !important;
}

.js-plotly-plot .xaxislayer text,
.js-plotly-plot .yaxislayer text,
.js-plotly-plot .zaxislayer text {
    fill: #1a1a1a !important;
}

.js-plotly-plot .legend text {
    fill: #1a1a1a !important;
}

/* ========================================
   7. DROPDOWN & CALENDAR POPUPS
   ======================================== */

/* Dropdown/Selectbox Menu Options - ENHANCED VISIBILITY */
div[data-baseweb="popover"] {
    z-index: 9999 !important;
}

div[data-baseweb="popover"] div[role="listbox"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    border: 2px solid #d32f2f !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
    padding: 8px !important;
}

div[data-baseweb="popover"] li[role="option"] {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    margin: 4px 0 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    line-height: 1.5 !important;
}

div[data-baseweb="popover"] li[role="option"] div,
div[data-baseweb="popover"] li[role="option"] span {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

div[data-baseweb="popover"] li[role="option"]:hover {
    background-color: #ffebee !important;
    color: #b71c1c !important;
    transform: translateX(4px);
}

div[data-baseweb="popover"] li[role="option"]:hover div,
div[data-baseweb="popover"] li[role="option"]:hover span {
    color: #b71c1c !important;
}

div[data-baseweb="popover"] li[role="option"][aria-selected="true"] {
    background: linear-gradient(135deg, #ffcdd2 0%, #ffebee 100%) !important;
    color: #b71c1c !important;
    font-weight: 700 !important;
}

div[data-baseweb="popover"] li[role="option"][aria-selected="true"] div,
div[data-baseweb="popover"] li[role="option"][aria-selected="true"] span {
    color: #b71c1c !important;
    font-weight: 700 !important;
}

/* DatePicker Calendar Popup */
div[data-baseweb="popover"] [data-baseweb="calendar"] {
    background: #ffffff !important;
    border-radius: 16px !important;
    padding: 20px !important;
    border: 2px solid #d32f2f !important;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.2) !important;
}

/* Calendar header */
div[data-baseweb="calendar"] [data-baseweb="calendar-header"] {
    background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px !important;
    margin-bottom: 16px !important;
}

div[data-baseweb="calendar"] [data-baseweb="calendar-header"] * {
    color: white !important;
}

/* Month/Year select buttons */
div[data-baseweb="calendar"] button {
    color: white !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="calendar"] button:hover {
    background: rgba(255, 255, 255, 0.2) !important;
    border-radius: 8px !important;
}

/* Day labels */
div[data-baseweb="calendar"] [role="columnheader"] {
    color: #d32f2f !important;
    font-weight: 700 !important;
    padding: 10px !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
}

/* Individual date cells */
div[data-baseweb="calendar"] [role="gridcell"] {
    padding: 4px !important;
}

div[data-baseweb="calendar"] [role="gridcell"] > div {
    color: #1a1a1a !important;
    background-color: #ffffff !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
    font-weight: 500 !important;
}

/* Hovered date */
div[data-baseweb="calendar"] [role="gridcell"] > div:hover {
    background-color: #ffebee !important;
    color: #b71c1c !important;
    cursor: pointer !important;
    transform: scale(1.1);
}

/* Selected date */
div[data-baseweb="calendar"] [aria-selected="true"] > div {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4) !important;
}

/* Today's date */
div[data-baseweb="calendar"] [data-is-highlighted="true"]:not([aria-selected="true"]) > div {
    border: 2px solid #d32f2f !important;
    color: #d32f2f !important;
    font-weight: 700 !important;
}

/* Dates from other months */
div[data-baseweb="calendar"] [aria-disabled="true"] > div {
    color: #cccccc !important;
    background-color: #f9f9f9 !important;
}

/* ========================================
   8. ALERTS & NOTIFICATIONS
   ======================================== */

/* Alert boxes */
.stAlert {
    border-radius: 12px !important;
    padding: 18px 24px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    animation: fadeInDown 0.4s ease;
}

.stAlert * {
    font-size: 15px !important;
    font-weight: 500 !important;
}

/* Error */
[data-testid="stAlert"][data-baseweb="notification"][kind="error"] {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%) !important;
    border-left: 5px solid #c62828 !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="error"] * {
    color: #1a1a1a !important;
}

/* Warning */
[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%) !important;
    border-left: 5px solid #f57f17 !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] * {
    color: #1a1a1a !important;
}

/* Info */
[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
    border-left: 5px solid #1565c0 !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="info"] * {
    color: #1a1a1a !important;
}

/* Success */
[data-testid="stAlert"][data-baseweb="notification"][kind="success"] {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important;
    border-left: 5px solid #2e7d32 !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="success"] * {
    color: #1a1a1a !important;
}

/* ========================================
   9. FOOTER & MISC
   ======================================== */

/* Custom footer */
.footer {
    text-align: center;
    padding: 35px;
    margin-top: 50px;
    background: linear-gradient(135deg, #ffffff 0%, #fff5f5 100%);
    border-radius: 20px;
    box-shadow: 0 -6px 25px rgba(0, 0, 0, 0.08);
}

.footer h3 {
    color: #b71c1c !important;
    margin-bottom: 12px !important;
}

.footer p {
    color: #666;
    font-size: 14px;
    line-height: 1.6;
}

/* Loading indicator */
.stSpinner > div {
    border-color: #d32f2f !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
    border-radius: 12px;
    font-weight: 600;
    color: #b71c1c;
    border: 2px solid #ffcdd2;
    transition: all 0.3s ease;
}

.streamlit-expanderHeader:hover {
    background: #ffebee;
    border-color: #d32f2f;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #c62828 0%, #a71a1a 100%);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1.5rem;
    }
    
    .main-title h1 {
        font-size: 32px;
    }
    
    .main-title p {
        font-size: 16px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
}
</style>""", unsafe_allow_html=True)

# ====================
# SESSION STATE
# ====================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'hospital_id' not in st.session_state:
    st.session_state.hospital_id = None
if 'delete_requested' not in st.session_state:
    st.session_state.delete_requested = False


# ====================
# DATABASE CONNECTION
# ====================
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='blood_bank',
            user='root',
            password='Vidya@252005',  # UPDATE THIS WITH YOUR PASSWORD
            autocommit=True,
            charset='utf8mb4'
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(buffered=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return True
    except Error as e:
        st.error(f"Database error: {e}")
        return None if fetch else False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ====================
# HELPER FUNCTIONS
# ====================
def get_next_id(prefix, table, id_col):
    """Generate next auto-incremented ID"""
    try:
        total_length = 5
        prefix_len = len(prefix)
        pad_length = total_length - prefix_len
        
        query = f"""
            SELECT {id_col} 
            FROM {table} 
            WHERE {id_col} LIKE %s 
            ORDER BY CAST(SUBSTRING({id_col}, {prefix_len + 1}) AS UNSIGNED) DESC 
            LIMIT 1
        """
        
        like_prefix = f"{prefix}%"
        result = execute_query(query, (like_prefix,), fetch=True)
        
        next_num = 1
        if result and result[0] and result[0][0]:
            max_id_str = result[0][0]
            numeric_part_str = max_id_str[prefix_len:]
            
            if numeric_part_str.isdigit():
                current_num = int(numeric_part_str)
                next_num = current_num + 1
        
        next_num_str = str(next_num).zfill(pad_length)
        
        if len(next_num_str) > pad_length:
            st.error(f"ID Overflow Error: Cannot generate new ID for prefix '{prefix}'.")
            return None
            
        return f"{prefix}{next_num_str}"
    except Exception as e:
        st.error(f"Error generating ID: {e}")
        return None

@st.cache_data(ttl=60)
def fetch_donors_list():
    query = "SELECT Donor_ID, F_name, L_name FROM Donor ORDER BY F_name"
    donors = execute_query(query)
    if donors:
        return {f"{row[1]} {row[2]} (ID: {row[0]})": row[0] for row in donors}
    return {}

@st.cache_data(ttl=60)
def fetch_recipients_list():
    query = "SELECT Recipient_ID, F_name, L_name FROM Recipient ORDER BY F_name"
    recipients = execute_query(query)
    if recipients:
        return {f"{row[1]} {row[2]} (ID: {row[0]})": row[0] for row in recipients}
    return {}

@st.cache_data(ttl=60)
def fetch_hospitals_list():
    query = "SELECT Hospital_ID, Name FROM Hospital ORDER BY Name"
    hospitals = execute_query(query)
    if hospitals:
        return {f"{row[1]} (ID: {row[0]})": row[0] for row in hospitals}
    return {}

# ==================================================================
# ==================== LOGIN/REGISTER PAGE =========================
# ==================================================================
if not st.session_state.logged_in:
    st.markdown("""
        <div class="main-title">
            <h1>Community Blood Bank</h1>
            <p>Management System - Saving Lives Together</p>
        </div>""", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.warning("Please enter both username and password.")
                else:
                    result = execute_query(
                        "SELECT User_ID, Password, Hospital_ID FROM User_Login WHERE Username = %s",
                        (username,)
                    )
                    
                    if result and len(result) > 0:
                        user_data = result[0]
                        user_id = user_data[0]
                        hashed_password = user_data[1]
                        hospital_id = user_data[2]
                        
                        if verify_password(password, hashed_password):
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.session_state.hospital_id = hospital_id
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
                    else:
                        st.error("Invalid username or password.")
    
    with tab2:
        st.markdown("### Register New Hospital & User")
        with st.form("register_form"):
            st.markdown("#### Hospital Information")
            col1, col2 = st.columns(2)
            with col1:
                h_name = st.text_input("Hospital Name", placeholder="City General Hospital")
                h_contact = st.text_input("Hospital Contact", placeholder="1234567890")
                h_email = st.text_input("Hospital Email", placeholder="hospital@email.com")
            with col2:
                h_address = st.text_area("Hospital Address", placeholder="Enter hospital address")
            
            st.markdown("#### User Account Information")
            col3, col4 = st.columns(2)
            with col3:
                u_username = st.text_input("Username", placeholder="Choose a username")
                u_password = st.text_input("Password", type="password", placeholder="Create a password")
                u_password_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            with col4:
                u_contact = st.text_input("Your Contact", placeholder="9876543210")
                u_email = st.text_input("Your Email", placeholder="user@email.com")
            
            submitted = st.form_submit_button("Register", type="primary", use_container_width=True)
            
            if submitted:
                if not all([h_name, h_contact, h_address, h_email, u_username, u_password, u_contact, u_email]):
                    st.warning("Please fill all required fields.")
                elif len(u_password) < 8:
                    st.warning("Password should be at least 8 characters long.")
                elif u_password != u_password_confirm:
                    st.error("Passwords do not match. Please try again.")
                else:
                    try:
                        hospital_id = get_next_id("H", "Hospital", "Hospital_ID")
                        new_user_id = get_next_id("U", "User_Login", "User_ID")
                        
                        if not hospital_id or not new_user_id:
                            st.error("Could not generate IDs. Please try again.")
                        else:
                            hashed_pwd = get_password_hash(u_password)
                            
                            execute_query(
                                "INSERT INTO Hospital (Hospital_ID, Name, Address) VALUES (%s, %s, %s)",
                                (hospital_id, h_name, h_address),
                                fetch=False
                            )
                            execute_query(
                                "INSERT INTO Hospital_Contact (Hospital_ID, Contact) VALUES (%s, %s)",
                                (hospital_id, h_contact),
                                fetch=False
                            )
                            execute_query(
                                "INSERT INTO Hospital_Email (Hospital_ID, Email) VALUES (%s, %s)",
                                (hospital_id, h_email),
                                fetch=False
                            )
                            execute_query(
                                "INSERT INTO User_Login (User_ID, Username, Password, Hospital_ID) VALUES (%s, %s, %s, %s)",
                                (new_user_id, u_username, hashed_pwd, hospital_id),
                                fetch=False
                            )
                            execute_query(
                                "INSERT INTO User_Contact (User_ID, Contact) VALUES (%s, %s)",
                                (new_user_id, u_contact),
                                fetch=False
                            )
                            execute_query(
                                "INSERT INTO User_Email (User_ID, Email) VALUES (%s, %s)",
                                (new_user_id, u_email),
                                fetch=False
                            )
                            
                            st.success(f"Hospital '{h_name}' and user '{u_username}' registered successfully!")
                            st.info("Please use the Login tab to access your account.")
                            st.balloons()
            
                    except Exception as e:
                        st.error(f"Registration failed: {e}")

# ==================================================================
# ==================== MAIN APPLICATION (Logged In) ================
# ==================================================================
if st.session_state.logged_in:
    
    # ====================
    # SIDEBAR
    # ====================
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3209/3209265.png", width=100)
        st.markdown("<h2 style='text-align: center; margin-top: 15px; color: white;'>Blood Bank System</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        pages = {
            "Dashboard": "Dashboard",
            "Donors": "Donors",
            "Recipients": "Recipients",
            "Donations": "Donations",
            "Requests": "Requests",
            "Hospitals": "Hospitals",
            "Analytics": "Analytics"
        }
        
        for page_key, page_name in pages.items():
            if st.button(f"{page_name}", key=page_key, use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()

        st.markdown("---")
        st.markdown(f"<p style='padding-left: 10px; color: rgba(255,255,255,0.8);'>Logged in as: <b>{st.session_state.username}</b></p>", unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True, key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.hospital_id = None
            st.session_state.current_page = "Dashboard"
            st.rerun()
            
        if st.button("Delete This User Account", use_container_width=True, key="delete_account_btn"):
            st.session_state.delete_requested = not st.session_state.get("delete_requested", False)

        if st.session_state.get("delete_requested", False):
            st.warning("This will permanently delete your account.")
            with st.form("modal_delete_form"):
                confirm_checkbox = st.checkbox("I understand this action is permanent.", key="delete_modal_confirm_cb")
                modal_submit = st.form_submit_button("Delete Account", type="secondary")
                
                if modal_submit:
                    if not confirm_checkbox:
                        st.error("Please check the confirmation box.")
                    else:
                        try:
                            uid = st.session_state.user_id
                            if uid:
                                execute_query("DELETE FROM User_Contact WHERE User_ID = %s", (uid,), fetch=False)
                                execute_query("DELETE FROM User_Email WHERE User_ID = %s", (uid,), fetch=False)
                                success_del = execute_query("DELETE FROM User_Login WHERE User_ID = %s", (uid,), fetch=False)
                                
                                if success_del:
                                    st.success("Account deleted. Logging out...")
                                    st.session_state.logged_in = False
                                    st.session_state.user_id = None
                                    st.session_state.hospital_id = None
                                    st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

        st.markdown("""
            <div style='padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 20px;'>
                <p style='font-size: 14px; text-align: center; margin: 0;'><b>Donate Blood</b></p>
                <p style='font-size: 13px; text-align: center; margin-top: 5px;'>Save Lives Today!</p>
            </div>
        """, unsafe_allow_html=True)

    # ====================
    # MAIN TITLE
    # ====================
    st.markdown("""
        <div class="main-title">
            <h1>Community Blood Bank</h1>
            <p>Management System - Saving Lives Together</p>
        </div>""", unsafe_allow_html=True)

    page = st.session_state.current_page

    # =========================================================
    # ==================== DASHBOARD PAGE =====================
    # =========================================================
    if page == "Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        
        result = execute_query("SELECT COUNT(*) FROM Donor")
        total_donors = result[0][0] if result else 0
        col1.metric("Total Donors", total_donors, delta="Active")
        
        result = execute_query("SELECT COUNT(*) FROM Recipient")
        total_recipients = result[0][0] if result else 0
        col2.metric("Recipients", total_recipients)
        
        result = execute_query("SELECT COUNT(*) FROM Donation")
        total_donations = result[0][0] if result else 0
        col3.metric("Donations", total_donations)
        
        result = execute_query("SELECT COUNT(*) FROM Request WHERE Status = 'Pending'")
        pending_requests = result[0][0] if result else 0
        col4.metric("Pending", pending_requests, delta=f"{pending_requests} Urgent", delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Blood Group Distribution")
            blood_data = execute_query("SELECT Blood_Group, COUNT(*) as count FROM Donor GROUP BY Blood_Group")
            
            if blood_data:
                df_blood = pd.DataFrame(blood_data, columns=['Blood Group', 'Count'])
                fig = px.pie(df_blood, values='Count', names='Blood Group', 
                            color_discrete_sequence=['#b71c1c', '#c62828', '#d32f2f', '#e53935', '#ef5350', '#e57373', '#ef9a9a', '#ffcdd2'],
                            hole=0.5)
                fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True, height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No donor data available.")

        with col2:
            st.markdown("### Monthly Donations")
            monthly_data = execute_query("""
                SELECT DATE_FORMAT(Donation_date, '%Y-%m') as month, COUNT(*) as count 
                FROM Donation GROUP BY month ORDER BY month DESC LIMIT 6
            """)
            
            if monthly_data:
                df_monthly = pd.DataFrame(monthly_data, columns=['Month', 'Donations'])
                fig = px.bar(df_monthly, x='Month', y='Donations', color='Donations',
                            color_continuous_scale=['#ffcdd2', '#d32f2f'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No monthly data available.")

        st.markdown("### Recent Activities")
        tab1, tab2 = st.tabs(["Recent Donations", "Recent Requests"])
        
        with tab1:
            recent_donations = execute_query("""
                SELECT d.Donation_ID, CONCAT(don.F_name, ' ', don.L_name) as Donor, 
                    h.Name as Hospital, d.Quantity, d.Donation_date
                FROM Donation d
                JOIN Donor don ON d.Donor_ID = don.Donor_ID
                JOIN Hospital h ON d.Hospital_ID = h.Hospital_ID
                ORDER BY d.Donation_date DESC LIMIT 5
            """)
            
            if recent_donations:
                df_donations = pd.DataFrame(recent_donations, columns=['ID', 'Donor', 'Hospital', 'Quantity (ml)', 'Date'])
                st.dataframe(df_donations, use_container_width=True, hide_index=True)
            else:
                st.info("No recent donations found.")

        with tab2:
            recent_requests = execute_query("""
                SELECT r.Request_ID, CONCAT(rec.F_name, ' ', rec.L_name) as Recipient, 
                    r.Blood_Group, r.Quantity, r.Status, r.Request_date
                FROM Request r
                JOIN Recipient rec ON r.Recipient_ID = rec.Recipient_ID
                ORDER BY r.Request_date DESC LIMIT 5
            """)
            
            if recent_requests:
                df_requests = pd.DataFrame(recent_requests, columns=['ID', 'Recipient', 'Blood Group', 'Quantity (ml)', 'Status', 'Date'])
                st.dataframe(df_requests, use_container_width=True, hide_index=True)
            else:
                st.info("No recent requests found.")

    # =========================================================
    # ===================== DONORS PAGE =======================
    # =========================================================
    elif page == "Donors":
        st.markdown("### Donor Management")
        
        tab1, tab2, tab3 = st.tabs(["View Donors", "Add Donor", "Search Donor"])
        
        with tab1:
            donors = execute_query("""
                SELECT d.Donor_ID, CONCAT(d.F_name, ' ', d.L_name) as Name, 
                    d.Gender, d.Age, d.Blood_Group, d.Address,
                    GROUP_CONCAT(dc.Contact SEPARATOR ', ') as Contacts
                FROM Donor d
                LEFT JOIN Donor_Contact dc ON d.Donor_ID = dc.Donor_ID
                GROUP BY d.Donor_ID
                ORDER BY d.Donor_ID
            """)
            
            if donors:
                df_donors = pd.DataFrame(donors, columns=['ID', 'Name', 'Gender', 'Age', 'Blood Group', 'Address', 'Contacts'])
                st.dataframe(df_donors, use_container_width=True, hide_index=True)
            else:
                st.info("No donors found in the database.")

        with tab2:
            st.markdown("#### Add New Donor")
            
            with st.form("add_donor_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    fname = st.text_input("First Name", placeholder="John")
                    lname = st.text_input("Last Name", placeholder="Doe")
                    gender = st.selectbox("Gender", ["M", "F", "Other"])
                
                with col2:
                    dob = st.date_input("Date of Birth", max_value=date.today(), value=date(2000, 1, 1))
                    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                    contact = st.text_input("Contact", placeholder="9876543210")
                
                address = st.text_area("Address", placeholder="Enter full address")
                
                submitted = st.form_submit_button("Add Donor", type="primary", use_container_width=True)
                
                if submitted:
                    if not fname or not lname or not contact:
                        st.warning("Please fill all required fields (Name, Contact).")
                    else:
                        donor_id = get_next_id("D", "Donor", "Donor_ID")
                        if not donor_id:
                            st.error("Could not generate Donor ID.")
                        else:
                            success = execute_query("""
                                INSERT INTO Donor (Donor_ID, F_name, L_name, Address, Gender, DOB, Age, Blood_Group)
                                VALUES (%s, %s, %s, %s, %s, %s, Calculate_Age(%s), %s)
                            """, (donor_id, fname, lname, address, gender, dob, dob, blood_group), fetch=False)
                            
                            if success:
                                execute_query("""
                                    INSERT INTO Donor_Contact (Donor_ID, Contact)
                                    VALUES (%s, %s)
                                """, (donor_id, contact), fetch=False)
                                
                                st.success(f"Donor added successfully! New ID: {donor_id}")
                                st.balloons()
                                st.cache_data.clear()
                            else:
                                st.error("Failed to add donor.")

        with tab3:
            st.markdown("#### Search Donor")
            
            search_option = st.selectbox("Search by", ["Donor ID", "Blood Group"], label_visibility="collapsed")
            
            if search_option == "Donor ID":
                col1, col2 = st.columns([3, 1])
                with col1:
                    search_id = st.text_input("Enter Donor ID", label_visibility="collapsed", placeholder="Enter Donor ID")
                with col2:
                    search_btn = st.button("Search", use_container_width=True)
                
                if search_btn and search_id:
                    result = execute_query("""
                        SELECT d.*, GROUP_CONCAT(dc.Contact SEPARATOR ', ')
                        FROM Donor d
                        LEFT JOIN Donor_Contact dc ON d.Donor_ID = dc.Donor_ID
                        WHERE d.Donor_ID = %s
                        GROUP BY d.Donor_ID
                    """, (search_id,))
                    
                    if result:
                        r = result[0]
                        st.success("Donor Found!")
                        st.markdown(f"""
                            <div class="section-card">
                                <h3 style='color: #b71c1c; margin-top: 0;'>{r[1]} {r[2]}</h3>
                                <p><strong>ID:</strong> {r[0]} | <strong>Gender:</strong> {r[4]} | <strong>Age:</strong> {r[6]}</p>
                                <p><strong>Blood Group:</strong> <span style='color: #d32f2f; font-size: 20px; font-weight: 700;'>{r[7]}</span></p>
                                <p><strong>Contact(s):</strong> {r[8] if r[8] else 'N/A'}</p>
                                <p><strong>Address:</strong> {r[3]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Donor not found")
            else:
                st.markdown("**Select Blood Group:**")
                blood_group_search = st.radio(
                    "Blood Group",
                    ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                results = execute_query("CALL GetDonorsByBloodGroup(%s)", (blood_group_search,))
                
                if results:
                    st.markdown(f"### Donors with Blood Group: {blood_group_search}")
                    df_results = pd.DataFrame(results, columns=['ID', 'First Name', 'Last Name', 'Age', 'Blood Group'])
                    st.dataframe(df_results, use_container_width=True, hide_index=True)
                else:
                    st.info("No donors found with this blood group")

    # =========================================================
    # =================== RECIPIENTS PAGE =====================
    # =========================================================
    elif page == "Recipients":
        st.markdown("### Recipient Management")
        
        tab1, tab2 = st.tabs(["View Recipients", "Add Recipient"])
        
        with tab1:
            recipients = execute_query("""
                SELECT r.Recipient_ID, CONCAT(r.F_name, ' ', r.L_name) as Name, 
                    r.Gender, r.Age, r.Blood_Group, r.Address,
                    GROUP_CONCAT(rc.Contact SEPARATOR ', ') as Contacts
                FROM Recipient r
                LEFT JOIN Recipient_Contact rc ON r.Recipient_ID = rc.Recipient_ID
                GROUP BY r.Recipient_ID
                ORDER BY r.Recipient_ID
            """)
            
            if recipients:
                df_recipients = pd.DataFrame(recipients, columns=['ID', 'Name', 'Gender', 'Age', 'Blood Group', 'Address', 'Contacts'])
                st.dataframe(df_recipients, use_container_width=True, hide_index=True)
            else:
                st.info("No recipients found in the database.")

        with tab2:
            st.markdown("#### Add New Recipient")
            
            with st.form("add_recipient_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    fname = st.text_input("First Name", placeholder="Jane")
                    lname = st.text_input("Last Name", placeholder="Smith")
                    gender = st.selectbox("Gender", ["M", "F", "Other"])
                
                with col2:
                    age = st.number_input("Age", min_value=1, max_value=120, value=30)
                    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                    contact = st.text_input("Contact", placeholder="9876543210")
                
                address = st.text_area("Address", placeholder="Enter full address")
                
                submitted = st.form_submit_button("Add Recipient", type="primary", use_container_width=True)
                
                if submitted:
                    if not fname or not lname or not contact:
                        st.warning("Please fill all required fields.")
                    else:
                        recipient_id = get_next_id("R", "Recipient", "Recipient_ID")
                        if not recipient_id:
                            st.error("Could not generate Recipient ID.")
                        else:
                            success = execute_query("""
                                INSERT INTO Recipient (Recipient_ID, F_name, L_name, Address, Gender, Age, Blood_Group)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """, (recipient_id, fname, lname, address, gender, age, blood_group), fetch=False)
                            
                            if success:
                                execute_query("""
                                    INSERT INTO Recipient_Contact (Recipient_ID, Contact)
                                    VALUES (%s, %s)
                                """, (recipient_id, contact), fetch=False)
                                
                                st.success(f"Recipient added successfully! New ID: {recipient_id}")
                                st.balloons()
                                st.cache_data.clear()
                            else:
                                st.error("Failed to add recipient.")

    # =========================================================
    # =================== DONATIONS PAGE ======================
    # =========================================================
    elif page == "Donations":
        st.markdown("### Donation Management")
        
        tab1, tab2 = st.tabs(["View Donations", "Record Donation"])
        
        with tab1:
            donations = execute_query("""
                SELECT d.Donation_ID, CONCAT(don.F_name, ' ', don.L_name) as Donor, 
                    don.Blood_Group, h.Name as Hospital, d.Quantity, d.Donation_date
                FROM Donation d
                JOIN Donor don ON d.Donor_ID = don.Donor_ID
                JOIN Hospital h ON d.Hospital_ID = h.Hospital_ID
                ORDER BY d.Donation_date DESC
            """)
            
            if donations:
                df_donations = pd.DataFrame(donations, 
                                            columns=['ID', 'Donor', 'Blood Group', 'Hospital', 'Quantity (ml)', 'Date'])
                st.dataframe(df_donations, use_container_width=True, hide_index=True)
            else:
                st.info("No donations found.")

        with tab2:
            st.markdown("#### Record New Donation")
            
            donors_dict = fetch_donors_list()
            hospitals_dict = fetch_hospitals_list()
            
            if not donors_dict or not hospitals_dict:
                st.warning("Please add at least one Donor and one Hospital.")
            else:
                with st.form("add_donation_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        donor_name = st.selectbox("Select Donor", options=donors_dict.keys())
                        hospital_name = st.selectbox("Select Hospital", options=hospitals_dict.keys())
                    
                    with col2:
                        quantity = st.number_input("Quantity (ml)", min_value=100, max_value=500, value=450, step=50)
                        donation_date = st.date_input("Donation Date", value=date.today())
                    
                    submitted = st.form_submit_button("Record Donation", type="primary", use_container_width=True)
                    
                    if submitted:
                        if not donor_name or not hospital_name:
                            st.warning("Please fill all required fields.")
                        else:
                            donation_id = get_next_id("DON", "Donation", "Donation_ID")
                            if not donation_id:
                                st.error("Could not generate Donation ID.")
                            else:
                                donor_id = donors_dict[donor_name]
                                hospital_id = hospitals_dict[hospital_name]
                                
                                success = execute_query("""
                                    INSERT INTO Donation (Donation_ID, Hospital_ID, Donor_ID, Quantity, Donation_date)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (donation_id, hospital_id, donor_id, quantity, donation_date), fetch=False)
                                
                                if success:
                                    st.success(f"Donation recorded successfully! New ID: {donation_id}")
                                    st.balloons()
                                    st.cache_data.clear()
                                else:
                                    st.error("Failed to record donation.")

    # =========================================================
    # ==================== REQUESTS PAGE ======================
    # =========================================================
    elif page == "Requests":
        st.markdown("### Blood Request Management")
        
        tab1, tab2, tab3 = st.tabs(["View Requests", "New Request", "Update Status"])
        
        with tab1:
            requests = execute_query("""
                SELECT r.Request_ID, CONCAT(rec.F_name, ' ', rec.L_name) as Recipient,
                    h.Name as Hospital, r.Blood_Group, r.Quantity, r.Status, r.Request_date
                FROM Request r
                JOIN Recipient rec ON r.Recipient_ID = rec.Recipient_ID
                JOIN Hospital h ON r.Hospital_ID = h.Hospital_ID
                ORDER BY r.Request_date DESC
            """)
            
            if requests:
                df_requests = pd.DataFrame(requests, 
                                        columns=['ID', 'Recipient', 'Hospital', 'Blood Group', 'Quantity (ml)', 'Status', 'Date'])
                st.dataframe(df_requests, use_container_width=True, hide_index=True)
            else:
                st.info("No requests found.")

        with tab2:
            st.markdown("#### Create New Blood Request")
            
            recipients_dict = fetch_recipients_list()
            hospitals_dict = fetch_hospitals_list()
            
            if not recipients_dict or not hospitals_dict:
                st.warning("Please add at least one Recipient and one Hospital.")
            else:
                with st.form("add_request_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        recipient_name = st.selectbox("Select Recipient", options=recipients_dict.keys())
                        hospital_name = st.selectbox("Select Hospital", options=hospitals_dict.keys())
                    
                    with col2:
                        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                        quantity = st.number_input("Quantity (ml)", min_value=100, max_value=2000, value=500, step=100)
                        request_date = st.date_input("Request Date", value=date.today())
                    
                    submitted = st.form_submit_button("Submit Request", type="primary", use_container_width=True)
                    
                    if submitted:
                        if not recipient_name or not hospital_name:
                            st.warning("Please fill all required fields.")
                        else:
                            request_id = get_next_id("REQ", "Request", "Request_ID")
                            if not request_id:
                                st.error("Could not generate Request ID.")
                            else:
                                recipient_id = recipients_dict[recipient_name]
                                hospital_id = hospitals_dict[hospital_name]
                                
                                success = execute_query("""
                                    INSERT INTO Request (Request_ID, Hospital_ID, Recipient_ID, Status, Quantity, Blood_Group, Request_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (request_id, hospital_id, recipient_id, 'Pending', quantity, blood_group, request_date), fetch=False)
                                
                                if success:
                                    st.success(f"Request submitted successfully! New ID: {request_id}")
                                    st.balloons()
                                    st.cache_data.clear()
                                else:
                                    st.error("Failed to submit request.")
                                
        with tab3:
            st.markdown("#### Update Request Status")
            
            pending_requests = execute_query("SELECT Request_ID FROM Request WHERE Status = 'Pending' ORDER BY Request_ID")
            
            if pending_requests:
                pending_request_ids = [req[0] for req in pending_requests]
                
                with st.form("update_request_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        request_to_update = st.selectbox("Select Pending Request ID", pending_request_ids)
                    with col2:
                        new_status = st.selectbox("New Status", ["Fulfilled", "Cancelled"])
                    
                    update_btn = st.form_submit_button("Update Status", type="primary", use_container_width=True)
                    
                    if update_btn:
                        success = execute_query("UPDATE Request SET Status = %s WHERE Request_ID = %s", (new_status, request_to_update), fetch=False)
                        if success:
                            st.success(f"Request {request_to_update} status updated to {new_status}.")
                            st.rerun()
                        else:
                            st.error("Failed to update status.")
            else:
                st.info("No pending requests to update.")

    # =========================================================
    # =================== HOSPITALS PAGE ======================
    # =========================================================
    elif page == "Hospitals":
        st.markdown("### Hospital Management")
        
        st.info("To add a new hospital, please log out and use the 'Register New Hospital' tab on the login page.")
        
        hospitals = execute_query("""
            SELECT h.Hospital_ID, h.Name, h.Address,
                   GROUP_CONCAT(DISTINCT hc.Contact SEPARATOR ', ') as Contacts,
                   GROUP_CONCAT(DISTINCT he.Email SEPARATOR ', ') as Emails
            FROM Hospital h
            LEFT JOIN Hospital_Contact hc ON h.Hospital_ID = hc.Hospital_ID
            LEFT JOIN Hospital_Email he ON h.Hospital_ID = he.Hospital_ID
            GROUP BY h.Hospital_ID
            ORDER BY h.Name
        """)
        
        if hospitals:
            df_hospitals = pd.DataFrame(hospitals, columns=['ID', 'Name', 'Address', 'Contacts', 'Emails'])
            st.dataframe(df_hospitals, use_container_width=True, hide_index=True)
        else:
            st.info("No hospitals found in the database.")

    # =========================================================
    # =================== ANALYTICS PAGE ======================
    # =========================================================
    elif page == "Analytics":
        st.markdown("### Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Blood Stock (Donated vs Fulfilled)")
            
            donated_q = """
                SELECT d.Blood_Group, SUM(don.Quantity) as TotalDonated
                FROM Donor d
                JOIN Donation don ON d.Donor_ID = don.Donor_ID
                GROUP BY d.Blood_Group
            """
            donated_data = execute_query(donated_q)
            
            fulfilled_q = """
                SELECT Blood_Group, SUM(Quantity) as TotalFulfilled
                FROM Request
                WHERE Status = 'Fulfilled'
                GROUP BY Blood_Group
            """
            fulfilled_data = execute_query(fulfilled_q)
            
            if donated_data:
                df_donated = pd.DataFrame(donated_data, columns=['Blood Group', 'Donated'])
                
                if fulfilled_data:
                    df_fulfilled = pd.DataFrame(fulfilled_data, columns=['Blood Group', 'Fulfilled'])
                    df_stock = pd.merge(df_donated, df_fulfilled, on='Blood Group', how='outer').fillna(0)
                else:
                    df_stock = df_donated.copy()
                    df_stock['Fulfilled'] = 0
                    
                df_stock['Net Stock'] = df_stock['Donated'] - df_stock['Fulfilled']
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_stock['Blood Group'],
                    y=df_stock['Donated'],
                    name='Total Donated',
                    marker_color='#c62828'
                ))
                fig.add_trace(go.Bar(
                    x=df_stock['Blood Group'],
                    y=df_stock['Fulfilled'],
                    name='Total Fulfilled',
                    marker_color='#ef9a9a'
                ))
                
                fig.update_layout(
                    barmode='group',
                    title='Donations vs Fulfilled Requests',
                    xaxis_title='Blood Group',
                    yaxis_title='Quantity (ml)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    legend_title_text='Metric'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No donation data for stock analysis.")

        with col2:
            st.markdown("#### Hospital Activity")
            
            activity_q = """
                SELECT 
                    h.Name,
                    COUNT(DISTINCT d.Donation_ID) as TotalDonations,
                    COUNT(DISTINCT r.Request_ID) as TotalRequests
                FROM Hospital h
                LEFT JOIN Donation d ON h.Hospital_ID = d.Hospital_ID
                LEFT JOIN Request r ON h.Hospital_ID = r.Hospital_ID
                GROUP BY h.Name
                ORDER BY TotalDonations DESC, TotalRequests DESC
            """
            activity_data = execute_query(activity_q)
            
            if activity_data:
                df_activity = pd.DataFrame(activity_data, columns=['Hospital', 'Donations', 'Requests'])
                
                fig = px.bar(df_activity.melt(id_vars='Hospital'), 
                            x='Hospital', y='value', color='variable',
                            title='Donations and Requests by Hospital',
                            color_discrete_map={'Donations': '#d32f2f', 'Requests': '#ffcdd2'},
                            barmode='group')
                
                fig.update_layout(
                    xaxis_title='Hospital',
                    yaxis_title='Count',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    legend_title_text='Activity'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hospital activity data available.")

        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("#### Age Distribution")
        donor_ages = execute_query("SELECT Age FROM Donor")
        recipient_ages = execute_query("SELECT Age FROM Recipient")
        
        if donor_ages or recipient_ages:
            fig = go.Figure()
            
            if donor_ages:
                df_donor_age = pd.DataFrame(donor_ages, columns=['Age'])
                fig.add_trace(go.Histogram(
                    x=df_donor_age['Age'],
                    name='Donors',
                    marker_color='#b71c1c',
                    opacity=0.75
                ))
            
            if recipient_ages:
                df_recipient_age = pd.DataFrame(recipient_ages, columns=['Age'])
                fig.add_trace(go.Histogram(
                    x=df_recipient_age['Age'],
                    name='Recipients',
                    marker_color='#ffcdd2',
                    opacity=0.75
                ))
            
            fig.update_layout(
                barmode='overlay',
                title='Donor and Recipient Age Distribution',
                xaxis_title='Age',
                yaxis_title='Count',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400  
            )
            fig.update_traces(opacity=0.75)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No age data available for analysis.")

    # ====================
    # FOOTER
    # ====================
    st.markdown("""
        <hr>
        <div class="footer">
            <h3>Community Blood Bank System</h3>
            <p>Built with Streamlit and MySQL</p>
            <p>Your contribution can save a life. Donate blood today!</p>
        </div>
    """, unsafe_allow_html=True)
