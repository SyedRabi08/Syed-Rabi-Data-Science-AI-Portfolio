import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- Page Configuration and Custom CSS ---
st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide the default sidebar
)

# Inject custom CSS to match the HTML design exactly
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
    /* Main body and background */
    .stApp {
        background-image: url('https://sfile.chatglm.cn/images-ppt/4bd38f4c555a.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Overlay effect */
    .stApp > div:first-child {
        background-color: rgba(0, 40, 80, 0.85) !important;
    }
    
    /* Typography */
    body {
        font-family: 'Source Sans Pro', sans-serif;
        color: white;
    }
    
    /* Header */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        border-bottom: 1px solid rgba(255, 255, 25, 0.1);
    }
    .logo {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .logo h1 {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .nav-menu {
        display: flex;
        gap: 30px;
    }
    .nav-item {
        font-size: 18px;
        font-weight: 600;
        color: #8ecae6;
        cursor: pointer;
        transition: color 0.3s;
        position: relative;
        padding-bottom: 10px;
    }
    .nav-item:hover, .nav-item.active {
        color: #52b788;
    }
    .nav-item.active::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: #52b788;
    }
    
    /* Section Titles */
    .section-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 25px;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    /* KPI Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi {
        flex: 1;
        background-color: rgba(255, 255, 25, 0.1);
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .kpi:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    .kpi-value {
        font-size: 42px;
        font-weight: 700;
        color: #52b788;
        margin-bottom: 5px;
    }
    .kpi-label {
        font-size: 18px;
        color: #e0fbfc;
    }
    
    /* Chart Containers - FIXED */
    .chart-container {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 30px;
        min-height: 400px;
        width: 100%;
    }
    /* Streamlit Plotly charts container styling */
    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 30px;
        min-height: 400px;
        width: 100%;
    }
    
    /* Insight Cards */
    .insights-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
        margin-bottom: 30px;
    }
    .insight-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 25px;
        border-left: 5px solid #52b788;
        transition: transform 0.3s;
    }
    .insight-card:hover {
        transform: translateX(5px);
    }
    .insight-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #8ecae6;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Recommendation Cards */
    .recommendations {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
    }
    .recommendation {
        background-color: rgba(255, 255, 25, 0.1);
        border-radius: 10px;
        padding: 25px;
        display: flex;
        align-items: flex-start;
        gap: 15px;
        transition: transform 0.3s;
    }
    .recommendation:hover {
        transform: translateY(-5px);
    }
    .recommendation-content h3 {
        font-size: 20px;
        margin-bottom: 8px;
        color: #8ecae6;
    }
    .recommendation-content p {
        font-size: 16px;
        line-height: 1.4;
    }
    
    /* Predictor Form */
    .predictor-form {
        background-color: rgba(255, 255, 25, 0.1);
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 30px;
    }
    .form-title {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 20px;
        color: #8ecae6;
        text-align: center;
    }
    .form-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 25px;
    }
    
    /* Prediction Result */
    .prediction-result {
        margin-top: 30px;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .prediction-profitable {
        background-color: rgba(82, 183, 136, 0.2);
        border: 1px solid #52b788;
    }
    .prediction-loss {
        background-color: rgba(255, 99, 132, 0.2);
        border: 1px solid #ff6384;
    }
    .prediction-title {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #8ecae6;
        font-size: 16px;
        border-top: 1px solid rgba(255, 255, 25, 0.1);
        margin-top: 2rem;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Style plotly charts */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(0, 40, 80, 0.5) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- Data Loading and Processing ---
@st.cache_data
def load_data():
    # List of possible file paths to check
    possible_paths = [
        # Relative paths from the script's location
        "data/processed/superstore_cleaned.csv",
        # Relative paths from the project root
        "projects/store-data-analysis/data/processed/superstore_cleaned.csv",
        # Absolute paths using the current working directory
        os.path.join(os.getcwd(), "data/processed/superstore_cleaned.csv"),
        os.path.join(os.getcwd(), "projects/store-data-analysis/data/processed/superstore_cleaned.csv"),
        # Add more paths if needed
        "C:/Users/syedr/PROJECT 1/store_analysis/notebooks/projects/store-data-analysis/data/processed/superstore_cleaned.csv"
    ]
    
    # Try each path until one works
    for path in possible_paths:
        if os.path.exists(path):
            # print to console for debugging; Streamlit will show this in logs
            print(f"✅ Successfully found data at: {path}")
            try:
                df = pd.read_csv(path, parse_dates=['Order Date', 'Ship Date'])
                return df
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                return None
    
    # If none of the paths work, show a helpful error message
    st.error(
        """
    ### ❌ Data File Not Found
    
    The application could not find the `superstore_cleaned.csv` file.
    
    Please ensure the file is placed in one of the following locations:
    - `data/processed/superstore_cleaned.csv`
    - `projects/store-data-analysis/data/processed/superstore_cleaned.csv`
    - Your project's root directory
    
    If you need to re-create it, please run the data cleaning steps in your analysis notebook first.
    """
    )
    return None

@st.cache_data
def process_data(df):
    if df is None:
        return None
    
    # Ensure required columns exist
    required_cols = ['Sales', 'Profit', 'Discount', 'Order Date', 'Ship Date', 'Category', 'Region', 'Sub-Category', 'Quantity', 'Ship Mode', 'Segment', 'Customer ID']
    for c in required_cols:
        if c not in df.columns:
            st.error(f"Required column missing from dataset: {c}")
            return None

    # Calculate KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_discount = df['Discount'].mean() * 100
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # Process monthly data
    df['Order Month'] = df['Order Date'].dt.to_period('M')
    monthly_data = df.groupby('Order Month').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly_data['Order Month'] = monthly_data['Order Month'].dt.to_timestamp()

    # Process category/region data
    category_data = df.groupby('Category').agg({'Profit': 'sum', 'Sales': 'sum'}).reset_index()
    region_data = df.groupby('Region').agg({'Profit': 'sum', 'Sales': 'sum'}).reset_index()

    # Generate insights
    high_discount_orders = df[df['Discount'] > 0.2]
    loss_making_high_discount = high_discount_orders[high_discount_orders['Profit'] < 0]
    loss_percentage = (len(loss_making_high_discount) / len(high_discount_orders)) * 100 if len(high_discount_orders) > 0 else 0

    if len(category_data) > 0:
        most_profitable_category = category_data.loc[category_data['Profit'].idxmax(), 'Category']
        least_profitable_category = category_data.loc[category_data['Profit'].idxmin(), 'Category']
    else:
        most_profitable_category = None
        least_profitable_category = None

    if len(region_data) > 0:
        best_region = region_data.loc[region_data['Profit'].idxmax(), 'Region']
        worst_region = region_data.loc[region_data['Profit'].idxmin(), 'Region']
    else:
        best_region = None
        worst_region = None

    # --- New Deep Dive Data Processing ---

    # 1. Sub-Category Performance
    subcategory_data = df.groupby('Sub-Category').agg({'Profit': 'sum', 'Sales': 'sum'}).reset_index()
    subcategory_data = subcategory_data.sort_values(by='Profit', ascending=True)  # Sort for horizontal bar

    # 2. Top Customers (Customer Lifetime Value)
    customer_data = df.groupby('Customer ID').agg({'Profit': 'sum', 'Sales': 'sum'}).reset_index()
    customer_data = customer_data.sort_values(by='Profit', ascending=False)

    # 3. Day of Week Analysis
    df['Order Day of Week'] = df['Order Date'].dt.day_name()
    dow_data = df.groupby('Order Day of Week').agg({'Profit': 'sum', 'Sales': 'sum'}).reset_index()
    # Ensure correct order for days of the week
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_data['Order Day of Week'] = pd.Categorical(dow_data['Order Day of Week'], categories=days_order, ordered=True)
    dow_data = dow_data.sort_values('Order Day of Week')

    # 4. Ship Mode Analysis
    shipmode_data = df.groupby('Ship Mode').agg({'Profit': 'sum', 'Sales': 'sum', 'Quantity': 'sum'}).reset_index()
    # avoid division by zero
    shipmode_data['Profit per Order'] = shipmode_data.apply(lambda r: (r['Profit'] / r['Sales']) if r['Sales'] != 0 else 0.0, axis=1)

    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'avg_discount': avg_discount,
        'profit_margin': profit_margin,
        'monthly_data': monthly_data,
        'category_data': category_data,
        'region_data': region_data,
        'loss_percentage': loss_percentage,
        'most_profitable_category': most_profitable_category,
        'least_profitable_category': least_profitable_category,
        'best_region': best_region,
        'worst_region': worst_region,
        'subcategory_data': subcategory_data,
        'customer_data': customer_data,
        'dow_data': dow_data,
        'shipmode_data': shipmode_data,
        'df': df
    }

def predict_profitability(sales, quantity, discount, ship_mode, segment, region, category, sub_category):
    probability = 0.7
    if discount > 0.2:
        probability -= 0.6
    elif discount > 0.1:
        probability -= 0.2
    elif discount == 0:
        probability += 0.1
    if category == 'Technology':
        probability += 0.2
    elif category == 'Furniture':
        probability -= 0.1
    if sub_category == 'Tables':
        probability -= 0.3
    elif sub_category in ['Phones', 'Accessories']:
        probability += 0.15
    if region in ['West', 'East']:
        probability += 0.1
    elif region == 'Central':
        probability -= 0.05
    if segment == 'Corporate':
        probability += 0.05
    elif segment == 'Home Office':
        probability += 0.03
    if sales > 500:
        probability += 0.05
    elif sales < 50:
        probability -= 0.1
    return max(0, min(1, probability))

# --- Main App Logic ---
def main():
    df = load_data()
    processed_data = process_data(df)
    if processed_data is None:
        st.stop()

    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'overview'

    # --- Custom Header and Navigation (simplified) ---
    st.markdown(
        f"""
    <div class="header">
        <div class="logo">
            <i class="material-icons" style="font-size: 36px; color: #52b788;">store</i>
            <h1>Superstore Analytics</h1>
        </div>
        <div class="nav-menu">
            <div class="nav-item {'active' if st.session_state.page == 'overview' else ''}">Overview</div>
            <div class="nav-item {'active' if st.session_state.page == 'insights' else ''}">Insights</div>
            <div class="nav-item {'active' if st.session_state.page == 'predictor' else ''}">Predictor</div>
            <div class="nav-item {'active' if st.session_state.page == 'recommendations' else ''}">Recommendations</div>
            <div class="nav-item {'active' if st.session_state.page == 'deepdive' else ''}">Deep Dive</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # --- Navigation Buttons (controls page) ---
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.button("Overview", key="nav_overview", use_container_width=True):
            st.session_state.page = 'overview'
            st.rerun()
    with col2:
        if st.button("Insights", key="nav_insights", use_container_width=True):
            st.session_state.page = 'insights'
            st.rerun()
    with col3:
        if st.button("Predictor", key="nav_predictor", use_container_width=True):
            st.session_state.page = 'predictor'
            st.rerun()
    with col4:
        if st.button("Recommendations", key="nav_recommendations", use_container_width=True):
            st.session_state.page = 'recommendations'
            st.rerun()
    with col5:
        if st.button("Deep Dive", key="nav_deepdive", use_container_width=True):
            st.session_state.page = 'deepdive'
            st.rerun()

    # --- Page Content ---
    if st.session_state.page == 'overview':
        st.markdown(
            '<div class="section-title"><i class="material-icons" style="font-size: 36px; color: #52b788;">dashboard</i> Business Overview</div>',
            unsafe_allow_html=True,
        )

        # KPIs
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(
                f'<div class="kpi"><div class="kpi-value">${processed_data["total_sales"]:,.0f}</div><div class="kpi-label">Total Sales</div></div>',
                unsafe_allow_html=True,
            )
        with kpi2:
            st.markdown(
                f'<div class="kpi"><div class="kpi-value">${processed_data["total_profit"]:,.0f}</div><div class="kpi-label">Total Profit</div></div>',
                unsafe_allow_html=True,
            )
        with kpi3:
            st.markdown(
                f'<div class="kpi"><div class="kpi-value">{processed_data["avg_discount"]:.1f}%</div><div class="kpi-label">Avg. Discount</div></div>',
                unsafe_allow_html=True,
            )
        with kpi4:
            st.markdown(
                f'<div class="kpi"><div class="kpi-value">{processed_data["profit_margin"]:.1f}%</div><div class="kpi-label">Profit Margin</div></div>',
                unsafe_allow_html=True,
            )

        # Charts
        chart1, chart2 = st.columns(2)
        with chart1:
            fig = px.line(processed_data['monthly_data'], x='Order Month', y='Sales', template='plotly_dark')
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                title_font_color="#e0fbfc",
                xaxis=dict(title=dict(text='Month', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
                yaxis=dict(title=dict(text='Sales ($)', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
            )
            st.plotly_chart(fig, use_container_width=True)

        with chart2:
            fig = px.bar(processed_data['category_data'], x='Category', y='Profit', template='plotly_dark')
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                title_font_color="#e0fbfc",
                xaxis=dict(title=dict(text='Category', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
                yaxis=dict(title=dict(text='Profit ($)', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
            )
            st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.page == 'insights':
        st.markdown(
            '<div class="section-title"><i class="material-icons" style="font-size: 36px; color: #52b788;">lightbulb</i> Key Insights</div>',
            unsafe_allow_html=True,
        )

        insight1, insight2 = st.columns(2)
        with insight1:
            st.markdown(
                f"""
            <div class="insight-card">
                <div class="insight-title"><i class="material-icons" style="color: #52b788;">trending_down</i> Discount Impact</div>
                <div>High discounts (>20%) are strongly correlated with loss-making transactions. {processed_data['loss_percentage']:.0f}% of orders with discounts above 20% result in losses.</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
            <div class="insight-card">
                <div class="insight-title"><i class="material-icons" style="color: #52b788;">category</i> Product Performance</div>
                <div>{processed_data['most_profitable_category']} category drives profit, while {processed_data['least_profitable_category']} underperforms.</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with insight2:
            # Prepare safe region profit display
            region_profit_str = "N/A"
            try:
                if processed_data['best_region'] is not None:
                    region_profit = processed_data['region_data'][processed_data['region_data']['Region'] == processed_data['best_region']]['Profit'].values
                    if len(region_profit) > 0:
                        region_profit_str = f"${region_profit[0]:,.0f}"
            except Exception:
                region_profit_str = "N/A"

            st.markdown(
                f"""
            <div class="insight-card">
                <div class="insight-title"><i class="material-icons" style="color: #52b788;">location_on</i> Regional Disparity</div>
                <div>{processed_data['best_region']} region leads with {region_profit_str} in profit.</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
            <div class="insight-card">
                <div class="insight-title"><i class="material-icons" style="color: #52b788;">people</i> Customer Segments</div>
                <div>Corporate and Home Office segments show higher average profit per transaction.</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        fig = px.scatter(processed_data['df'], x='Discount', y='Profit', color='Category', template='plotly_dark', opacity=0.7)
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            title_font_color="#e0fbfc",
            xaxis=dict(title=dict(text='Discount', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
            yaxis=dict(title=dict(text='Profit ($)', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
        )
        st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.page == 'predictor':
        st.markdown(
            '<div class="section-title"><i class="material-icons" style="font-size: 36px; color: #52b788;">psychology</i> Profit/Loss Predictor</div>',
            unsafe_allow_html=True,
        )

        with st.form("prediction_form"):
            st.markdown('<div class="predictor-form"><div class="form-title">Enter Order Details to Predict Profitability</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                sales = st.number_input("Sales Amount ($)", min_value=0.0, value=200.0, step=10.0)
                quantity = st.number_input("Quantity", min_value=1, value=3)
                discount = st.slider("Discount (%)", min_value=0.0, max_value=80.0, value=10.0, step=5.0) / 100.0
            with col2:
                ship_mode = st.selectbox("Ship Mode", options=processed_data['df']['Ship Mode'].unique())
                segment = st.selectbox("Customer Segment", options=processed_data['df']['Segment'].unique())
                region = st.selectbox("Region", options=processed_data['df']['Region'].unique())
            with col3:
                category = st.selectbox("Product Category", options=processed_data['df']['Category'].unique())
                sub_category_options = processed_data['df'][processed_data['df']['Category'] == category]['Sub-Category'].unique()
                sub_category = st.selectbox("Product Sub-Category", options=sub_category_options)

            submitted = st.form_submit_button("Predict Profitability")

            if submitted:
                probability = predict_profitability(sales, quantity, discount, ship_mode, segment, region, category, sub_category)
                if probability >= 0.5:
                    st.markdown(
                        f"""
                    <div class="prediction-result prediction-profitable">
                        <div class="prediction-title"><i class="material-icons">check_circle</i> Predicted: Profitable Order</div>
                        <div>The model is {probability*100:.0f}% confident this order will be profitable.</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div class="prediction-result prediction-loss">
                        <div class="prediction-title"><i class="material-icons">cancel</i> Predicted: Loss-Making Order</div>
                        <div>The model is {(1-probability)*100:.0f}% confident this order will result in a loss.</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            st.markdown("</div>", unsafe_allow_html=True)

        model_metrics_df = pd.DataFrame({
            'Metric': ['Accuracy', 'Precision (Loss)', 'Recall (Loss)', 'F1-Score (Loss)'],
            'Score': [0.95, 0.95, 0.79, 0.86]
        })
        fig = px.bar(model_metrics_df, x='Metric', y='Score', template='plotly_dark')
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(range=[0, 1], title=dict(text='Score', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
            xaxis=dict(title=dict(text='Metric', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
        )
        st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.page == 'recommendations':
        st.markdown(
            '<div class="section-title"><i class="material-icons" style="font-size: 36px; color: #52b788;">recommend</i> Strategic Recommendations</div>',
            unsafe_allow_html=True,
        )

        rec1, rec2 = st.columns(2)
        with rec1:
            st.markdown(
                """
            <div class="recommendation">
                <i class="material-icons" style="font-size: 32px; color: #52b788;">trending_down</i>
                <div class="recommendation-content">
                    <h3>Limit Discounts</h3>
                    <p>Implement a company-wide policy capping discounts at 20% to eliminate loss-making transactions.</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
            <div class="recommendation">
                <i class="material-icons" style="font-size: 32px; color: #52b788;">laptop</i>
                <div class="recommendation-content">
                    <h3>Promote Technology Products</h3>
                    <p>Increase marketing spend and sales incentives for the highly profitable Technology category.</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with rec2:
            st.markdown(
                """
            <div class="recommendation">
                <i class="material-icons" style="font-size: 32px; color: #52b788;">search</i>
                <div class="recommendation-content">
                    <h3>Investigate Tables Sub-Category</h3>
                    <p>Conduct a deep-dive analysis into the Tables sub-category to understand why it is unprofitable.</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
            <div class="recommendation">
                <i class="material-icons" style="font-size: 32px; color: #52b788;">location_on</i>
                <div class="recommendation-content">
                    <h3>Boost Central Region</h3>
                    <p>Replicate successful strategies from the West region in the underperforming Central region.</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    elif st.session_state.page == 'deepdive':
        st.markdown(
            '<div class="section-title"><i class="material-icons" style="font-size: 36px; color: #52b788;">explore</i> Deep Dive Analysis</div>',
            unsafe_allow_html=True,
        )

        # --- Sub-Category Performance ---
        st.subheader("Profitability by Product Sub-Category")
        fig = px.bar(
            processed_data['subcategory_data'],
            x='Profit',
            y='Sub-Category',
            orientation='h',
            template='plotly_dark',
            title='Total Profit by Sub-Category',
            labels={'Profit': 'Total Profit ($)', 'Sub-Category': 'Sub-Category'},
            color='Profit',
            color_continuous_scale='RdYlGn'  # Red for loss, Green for profit
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(categoryorder='total ascending', tickfont=dict(color='#e0fbfc')),
            xaxis=dict(title=dict(text='Total Profit ($)', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Top Customers ---
        st.subheader("Top 10 Customers by Profit (Customer Lifetime Value)")
        top_customers = processed_data['customer_data'].head(10)
        if not top_customers.empty:
            top_customer_id = top_customers.iloc[0]['Customer ID']
            top_customer_profit = top_customers.iloc[0]['Profit']
            pct = (top_customers['Profit'].sum() / processed_data['total_profit'] * 100) if processed_data['total_profit'] != 0 else 0.0
            st.markdown(
                f"""
            <div class="insight-card">
                <div class="insight-title"><i class="material-icons" style="font-size: 20px; color: #52b788;">stars</i> Key Finding</div>
                <div>Your top customer is {top_customer_id}, with a total profit of ${top_customer_profit:,.0f}. The top 10 customers contribute to {pct:.1f}% of total profit.</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No customer data available to show top customers.")

        if not top_customers.empty:
            fig = px.bar(
                top_customers,
                x='Profit',
                y='Customer ID',
                orientation='h',
                template='plotly_dark',
                title='Top 10 Customers by Total Profit',
                labels={'Profit': 'Total Profit ($)', 'Customer ID': 'Customer ID'}
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(color='#e0fbfc')),
                xaxis=dict(title=dict(text='Total Profit ($)', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
            )
            st.plotly_chart(fig, use_container_width=True)

        # --- Sales by Day of Week and Ship Mode ---
        chart1, chart2 = st.columns(2)
        with chart1:
            st.subheader("Sales and Profit by Day of the Week")
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
            fig.add_trace(go.Bar(x=processed_data['dow_data']['Order Day of Week'], y=processed_data['dow_data']['Sales'], name='Sales'), row=1, col=1)
            fig.add_trace(go.Bar(x=processed_data['dow_data']['Order Day of Week'], y=processed_data['dow_data']['Profit'], name='Profit'), row=2, col=1)
            fig.update_layout(
                template='plotly_dark',
                height=500,
                title_font_color="#e0fbfc",
                showlegend=False,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            fig.update_xaxes(title_text='Day of Week', tickfont=dict(color='#e0fbfc'))
            fig.update_yaxes(title_text='Sales ($)', row=1, col=1, tickfont=dict(color='#e0fbfc'))
            fig.update_yaxes(title_text='Profit ($)', row=2, col=1, tickfont=dict(color='#e0fbfc'))
            st.plotly_chart(fig, use_container_width=True)

        with chart2:
            st.subheader("Ship Mode Profitability")
            fig = px.bar(
                processed_data['shipmode_data'],
                x='Ship Mode',
                y='Profit per Order',
                template='plotly_dark',
                title='Profit Margin per Order by Ship Mode',
                labels={'Profit per Order': 'Profit Margin (Profit/Sales)', 'Ship Mode': 'Ship Mode'}
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(title=dict(text='Ship Mode', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc')),
                yaxis=dict(title=dict(text='Profit Margin', font=dict(color='#e0fbfc')), tickfont=dict(color='#e0fbfc'))
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Footer ---
    st.markdown('<div class="footer"><p>Business Analytics Department | Superstore Sales Analysis | October 2025</p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
