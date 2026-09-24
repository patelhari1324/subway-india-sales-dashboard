# ============================================================
#                    IMPORT LIBRARIES
# ============================================================

import os
import base64

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
#                    PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Subway India Executive Dashboard",
    page_icon="🥪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
#                    MATPLOTLIB COLORS
# ============================================================

plt.rcParams["text.color"] = "#006633"
plt.rcParams["axes.labelcolor"] = "#006633"
plt.rcParams["xtick.color"] = "#006633"
plt.rcParams["ytick.color"] = "#006633"
plt.rcParams["axes.titlecolor"] = "#006633"


# ============================================================
#                    IMAGE TO BASE64
# ============================================================

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# ============================================================
#                    LOAD LOGO
# ============================================================

logo_base64 = None

if os.path.exists("subway_logo.png"):
    logo_base64 = image_to_base64("subway_logo.png")


# ============================================================
#                    CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
background: linear-gradient(180deg, #FFF8E8 0%, #FFFDF7 50%, #F6F2E7 100%);
}

h1, h2, h3, h4, h5, h6 {
color: #006633 !important;
font-weight: 800 !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
color: #006633 !important;
}

[data-testid="stMarkdownContainer"] p {
color: #2D1B14 !important;
}

.block-container {
padding-top: 0.5rem !important;
padding-bottom: 2rem;
max-width: 1500px;
}

header[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.subway-header {
background: linear-gradient(135deg, #FFFDF7, #FFF8E8);
padding: 25px 20px 30px 20px;
text-align: center;
border-top: 8px solid #006633;
border-bottom: 8px solid #FFC72C;
border-radius: 0 0 28px 28px;
box-shadow: 0 8px 25px rgba(0, 102, 51, 0.12);
margin-bottom: 28px;
}

.subway-logo {
display: block;
width: 240px;
max-width: 70%;
max-height: 100px;
height: auto;
object-fit: contain;
margin: 0 auto;
}

.header-title {
color: #006633 !important;
font-size: 38px;
font-weight: 800;
margin-top: 18px;
}

.header-subtitle {
color: #2D1B14 !important;
font-size: 16px;
margin-top: 5px;
}

[data-testid="stSidebar"] {
background: linear-gradient(180deg, #FFFDF7, #FFF3D2);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
color: #006633 !important;
}

[data-testid="stSidebar"] label {
color: #006633 !important;
font-weight: 700 !important;
}

[data-testid="stSidebar"] p {
color: #2D1B14 !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] span {
color: #2D1B14 !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {
border: 1px solid #006633 !important;
border-radius: 10px;
}

[data-testid="stSidebar"] input {
color: #2D1B14 !important;
}

.section-title {
color: #006633 !important;
font-size: 24px;
font-weight: 800;
margin-top: 10px;
margin-bottom: 15px;
}

.kpi-card {
background: white;
border-radius: 22px;
padding: 20px 15px;
text-align: center;
border-top: 5px solid #FFC72C;
box-shadow: 0 10px 25px rgba(0,0,0,0.08);
min-height: 145px;
}

.kpi-icon-box {
width: 54px;
height: 54px;
margin: 0 auto 9px auto;
border-radius: 16px;
background: linear-gradient(135deg, #006633, #009639);
display: flex;
justify-content: center;
align-items: center;
}

.kpi-icon-box img {
width: 28px;
height: 28px;
}

.kpi-label {
color: #006633 !important;
font-size: 11px;
font-weight: 800;
letter-spacing: 1.8px;
}

.kpi-value {
color: #006633 !important;
font-size: 30px;
font-weight: 800;
margin-top: 5px;
}

.chart-card {
background: white;
border-radius: 22px;
padding: 18px;
border: 1px solid rgba(255, 199, 44, 0.25);
box-shadow: 0 10px 24px rgba(0,0,0,0.07);
margin-bottom: 20px;
}

.chart-card h1,
.chart-card h2,
.chart-card h3,
.chart-card h4 {
color: #006633 !important;
}

.chart-card [data-testid="stMarkdownContainer"] h3 {
color: #006633 !important;
font-weight: 800 !important;
}

[data-testid="stDataFrame"] {
border-radius: 14px;
}

.stDownloadButton button {
background: #006633 !important;
color: white !important;
border: none;
border-radius: 10px;
font-weight: 700;
}

.stDownloadButton button:hover {
background: #009639 !important;
color: white !important;
}

button {
color: white !important;
}

div[data-testid="stVerticalBlock"] {
gap: 0.6rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
#                    LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("Subway_Sales_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    return df


df = load_data()


# ============================================================
#                    SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🎛 Dashboard Filters")
st.sidebar.caption("Use the filters to explore sales performance.")

selected_city = st.sidebar.selectbox(
    "🏙 City",
    ["All"] + sorted(df["City"].dropna().unique().tolist()),
    key="filter_city"
)

selected_payment = st.sidebar.selectbox(
    "💳 Payment Method",
    ["All"] + sorted(df["Payment_Method"].dropna().unique().tolist()),
    key="filter_payment"
)

selected_meal = st.sidebar.selectbox(
    "🍽 Meal Time",
    ["All"] + sorted(df["Meal_Time"].dropna().unique().tolist()),
    key="filter_meal"
)

selected_customer = st.sidebar.selectbox(
    "👤 Customer Type",
    ["All"] + sorted(df["Customer_Type"].dropna().unique().tolist()),
    key="filter_customer"
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="filter_dates"
)


# ============================================================
#                    APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_payment != "All":
    filtered_df = filtered_df[filtered_df["Payment_Method"] == selected_payment]

if selected_meal != "All":
    filtered_df = filtered_df[filtered_df["Meal_Time"] == selected_meal]

if selected_customer != "All":
    filtered_df = filtered_df[filtered_df["Customer_Type"] == selected_customer]

if len(selected_dates) == 2:
    start_date = pd.to_datetime(selected_dates[0])
    end_date = pd.to_datetime(selected_dates[1])
    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
    ]


# ============================================================
#                    NO DATA CHECK
# ============================================================

if filtered_df.empty:
    st.warning("⚠ No data matches the selected filters.")
    st.stop()


# ============================================================
#                    KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Total_Sales"].sum()
total_orders = len(filtered_df)
avg_order = filtered_df["Total_Sales"].mean()
items_sold = filtered_df["Quantity"].sum()


# ============================================================
#                    KPI ICON FUNCTION
# ============================================================

def svg_to_data_uri(svg_code):
    encoded = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
    return "data:image/svg+xml;base64," + encoded


# ============================================================
#                    SALES ICON
# ============================================================

sales_svg = svg_to_data_uri("""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M12 2v20"/>
<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H7"/>
</svg>
""")


# ============================================================
#                    ORDERS ICON
# ============================================================

orders_svg = svg_to_data_uri("""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M6 2h12l2 5H4l2-5z"/>
<path d="M4 7h16v14H4z"/>
<path d="M8 11h8"/>
<path d="M8 15h5"/>
</svg>
""")


# ============================================================
#                    AVERAGE ICON
# ============================================================

average_svg = svg_to_data_uri("""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<rect x="4" y="2" width="16" height="20" rx="2"/>
<line x1="8" y1="6" x2="16" y2="6"/>
<line x1="8" y1="10" x2="10" y2="10"/>
<line x1="14" y1="10" x2="16" y2="10"/>
<line x1="8" y1="14" x2="10" y2="14"/>
<line x1="14" y1="14" x2="16" y2="14"/>
<line x1="8" y1="18" x2="10" y2="18"/>
<line x1="14" y1="18" x2="16" y2="18"/>
</svg>
""")


# ============================================================
#                    ITEMS ICON
# ============================================================

items_svg = svg_to_data_uri("""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M3 9h18"/>
<path d="M5 9l2-5h10l2 5"/>
<path d="M4 9v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9"/>
<path d="M8 13h8"/>
<path d="M10 16h4"/>
</svg>
""")


# ============================================================
#                    SUBWAY HEADER
# ============================================================

st.markdown('<div class="subway-header">', unsafe_allow_html=True)


# ============================================================
#                    SINGLE CENTER LOGO
# ============================================================

if logo_base64:
    st.markdown(
        f'<img src="data:image/png;base64,{logo_base64}" class="subway-logo">',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """<div style="color:#006633; font-size:42px; font-weight:900; text-align:center;">SUBWAY</div>""",
        unsafe_allow_html=True
    )


# ============================================================
#                    MAIN TITLE
# ============================================================

st.markdown(
    """<div class="header-title">Subway India Executive Dashboard</div>""",
    unsafe_allow_html=True
)


# ============================================================
#                    SUBTITLE
# ============================================================

st.markdown(
    """<div class="header-subtitle">Portfolio Project • Hari Patel</div>""",
    unsafe_allow_html=True
)


# Close header

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
#                    KPI SECTION
# ============================================================

st.markdown(
    """<div class="section-title">📊 Key Performance Indicators</div>""",
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


# ============================================================
#                    KPI 1 - SALES
# ============================================================

with c1:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-icon-box"><img src="{sales_svg}"></div>
<div class="kpi-label">TOTAL SALES</div>
<div class="kpi-value">₹{total_sales:,.0f}</div>
</div>""", unsafe_allow_html=True)


# ============================================================
#                    KPI 2 - ORDERS
# ============================================================

with c2:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-icon-box"><img src="{orders_svg}"></div>
<div class="kpi-label">TOTAL ORDERS</div>
<div class="kpi-value">{total_orders:,}</div>
</div>""", unsafe_allow_html=True)


# ============================================================
#                    KPI 3 - AVG ORDER
# ============================================================

with c3:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-icon-box"><img src="{average_svg}"></div>
<div class="kpi-label">AVG ORDER</div>
<div class="kpi-value">₹{avg_order:,.0f}</div>
</div>""", unsafe_allow_html=True)


# ============================================================
#                    KPI 4 - ITEMS
# ============================================================

with c4:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-icon-box"><img src="{items_svg}"></div>
<div class="kpi-label">ITEMS SOLD</div>
<div class="kpi-value">{items_sold:,}</div>
</div>""", unsafe_allow_html=True)

st.write("")


# ============================================================
#                    ANALYTICS SECTION
# ============================================================

st.markdown(
    """<div class="section-title">📈 Sales Analytics</div>""",
    unsafe_allow_html=True
)


# ============================================================
#                    CHART ROW 1
# ============================================================

row1_col1, row1_col2 = st.columns(2)


# ============================================================
#                    SALES BY CITY
# ============================================================

with row1_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("📍 Sales by City")

    city_sales = (
        filtered_df.groupby("City")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(6, 3.4))
    city_sales.plot(kind="bar", color="#009639", ax=ax1)
    ax1.set_xlabel("")
    ax1.set_ylabel("Sales ₹")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    plt.xticks(rotation=25)
    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
#                    DAILY SALES
# ============================================================

with row1_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("📈 Daily Sales Trend")

    daily_sales = (
        filtered_df.groupby("Date")["Total_Sales"]
        .sum()
        .sort_index()
    )

    fig2, ax2 = plt.subplots(figsize=(6, 3.4))
    daily_sales.plot(kind="line", marker="o", color="#006633", linewidth=2.5, ax=ax2)
    ax2.set_xlabel("")
    ax2.set_ylabel("Sales ₹")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    plt.xticks(rotation=25)
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
#                    CHART ROW 2
# ============================================================

row2_col1, row2_col2 = st.columns(2)


# ============================================================
#                    TOP PRODUCTS
# ============================================================

with row2_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("🥪 Top 5 Products")

    top_products = (
        filtered_df.groupby("Product_Name")["Quantity"]
        .sum()
        .sort_values()
        .tail(5)
    )

    fig3, ax3 = plt.subplots(figsize=(6, 3.4))
    top_products.plot(kind="barh", color="#FFC72C", ax=ax3)
    ax3.set_xlabel("Quantity Sold")
    ax3.set_ylabel("")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig3, use_container_width=True)
    plt.close(fig3)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
#                    PAYMENT METHODS
# ============================================================

with row2_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("💳 Payment Methods")

    payment_data = filtered_df["Payment_Method"].value_counts()

    fig4, ax4 = plt.subplots(figsize=(6, 3.4))

    colors = ["#006633", "#009639", "#FFC72C", "#8BC34A"]

    wedges, texts, autotexts = ax4.pie(
        payment_data.values,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        wedgeprops={"width": 0.42}
    )

    ax4.legend(
        wedges,
        payment_data.index,
        title="Payment Method",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    ax4.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig4, use_container_width=True)
    plt.close(fig4)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
#                    FILTERED DATA
# ============================================================

st.markdown(
    """<div class="section-title">📋 Filtered Sales Data</div>""",
    unsafe_allow_html=True
)

st.dataframe(filtered_df, use_container_width=True)


# ============================================================
#                    DOWNLOAD BUTTON
# ============================================================

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv_data,
    file_name="Filtered_Subway_Sales.csv",
    mime="text/csv"
)


# ============================================================
#                         END
# ============================================================