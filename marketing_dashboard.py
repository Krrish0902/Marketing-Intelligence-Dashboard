import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 0.4rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .positive-change {
        color: #28a745;
    }
    .negative-change {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache processed data"""
    try:
        combined_df = pd.read_csv('processed_combined.csv', index_col=0, parse_dates=True)
        daily_marketing = pd.read_csv('processed_daily_marketing.csv', parse_dates=['date'])
        marketing_df = pd.read_csv('processed_marketing.csv', parse_dates=['date'])
        business_df = pd.read_csv('processed_business.csv', parse_dates=['date'])
        return combined_df, daily_marketing, marketing_df, business_df
    except FileNotFoundError:
        st.error("Processed data files not found. Please run data_processing.py first.")
        return None, None, None, None

def create_kpi_card(title, value, change=None, format_type="number"):
    """Create a KPI card component"""
    if format_type == "currency":
        formatted_value = f"${value:,.0f}"
    elif format_type == "percentage":
        formatted_value = f"{value:.1%}"
    elif format_type == "decimal":
        formatted_value = f"{value:.2f}"
    else:
        formatted_value = f"{value:,.0f}"
    
    with st.container():
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{formatted_value}</div>
        </div>
        """, unsafe_allow_html=True)

def calculate_period_comparison(data, metric, current_period, previous_period):
    """Calculate percentage change between periods"""
    current_value = data[data.index.isin(current_period)][metric].sum()
    previous_value = data[data.index.isin(previous_period)][metric].sum()
    
    if previous_value == 0:
        return 0
    return ((current_value - previous_value) / previous_value) * 100

def create_executive_overview(combined_df):
    """Create Executive Overview dashboard"""
    st.markdown('<div class="main-header">📊 Executive Overview</div>', unsafe_allow_html=True)
    
    # Date range selector
    date_range = st.date_input(
        "Select Date Range",
        value=(combined_df.index.min().date(), combined_df.index.max().date()),
        min_value=combined_df.index.min().date(),
        max_value=combined_df.index.max().date()
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = combined_df[(combined_df.index.date >= start_date) & (combined_df.index.date <= end_date)]
        
        # Calculate previous period for comparison
        period_length = (end_date - start_date).days
        prev_start = start_date - timedelta(days=period_length)
        prev_end = start_date - timedelta(days=1)
        prev_data = combined_df[(combined_df.index.date >= prev_start) & (combined_df.index.date <= prev_end)]
        
        # Top-level KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_spend = filtered_data['total_spend'].sum()
            spend_change = calculate_period_comparison(combined_df, 'total_spend', 
                                                     filtered_data.index.date, prev_data.index.date)
            create_kpi_card("Total Spend", total_spend, spend_change, "currency")
        
        with col2:
            total_revenue = filtered_data['total revenue'].sum()
            revenue_change = calculate_period_comparison(combined_df, 'total revenue',
                                                       filtered_data.index.date, prev_data.index.date)
            create_kpi_card("Total Revenue", total_revenue, revenue_change, "currency")
        
        with col3:
            total_orders = filtered_data['# of orders'].sum()
            orders_change = calculate_period_comparison(combined_df, '# of orders',
                                                      filtered_data.index.date, prev_data.index.date)
            create_kpi_card("Total Orders", total_orders, orders_change, "number")
        
        with col4:
            avg_roas = filtered_data['total_roas'].mean()
            create_kpi_card("Average ROAS", avg_roas, None, "decimal")
        
        # Additional KPIs
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            gross_profit = filtered_data['gross profit'].sum()
            create_kpi_card("Gross Profit", gross_profit, None, "currency")
        
        with col6:
            avg_cac = filtered_data['total_cac'].mean()
            create_kpi_card("Average CAC", avg_cac, None, "currency")
        
        with col7:
            new_customers = filtered_data['new customers'].sum()
            create_kpi_card("New Customers", new_customers, None, "number")
        
        with col8:
            avg_aov = filtered_data['aov'].mean()
            create_kpi_card("Average AOV", avg_aov, None, "currency")
        
        # Charts
        st.markdown("## 📈 Key Trends")
        
        # Daily Spend vs Revenue
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig1.add_trace(
            go.Scatter(x=filtered_data.index, y=filtered_data['total_spend'], 
                      name="Daily Spend", line=dict(color='#ff7f0e')),
            secondary_y=False,
        )
        
        fig1.add_trace(
            go.Scatter(x=filtered_data.index, y=filtered_data['total revenue'], 
                      name="Daily Revenue", line=dict(color='#2ca02c')),
            secondary_y=True,
        )
        
        fig1.update_xaxes(title_text="Date")
        fig1.update_yaxes(title_text="Daily Spend ($)", secondary_y=False)
        fig1.update_yaxes(title_text="Daily Revenue ($)", secondary_y=True)
        fig1.update_layout(title_text="Daily Spend vs Daily Revenue", height=400)
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # ROAS Trend
        fig2 = px.line(filtered_data.reset_index(), x='date', y='total_roas',
                      title="ROAS Trend Over Time", height=400)
        fig2.update_layout(yaxis_title="ROAS")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Additional Key Metrics
        st.markdown("## 📊 Marketing Efficiency Metrics")
        
        col9, col10, col11, col12 = st.columns(4)
        
        with col9:
            total_impressions = filtered_data[['impressions_Facebook', 'impressions_Google', 'impressions_TikTok']].sum().sum()
            create_kpi_card("Total Impressions", total_impressions, None, "number")
        
        with col10:
            total_clicks = filtered_data[['clicks_Facebook', 'clicks_Google', 'clicks_TikTok']].sum().sum()
            create_kpi_card("Total Clicks", total_clicks, None, "number")
        
        with col11:
            overall_ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0
            create_kpi_card("Overall CTR", overall_ctr, None, "percentage")
        
        with col12:
            overall_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
            create_kpi_card("Overall CPC", overall_cpc, None, "decimal")
        
        # Marketing Efficiency Charts
        col13, col14 = st.columns(2)
        
        with col13:
            # Impressions vs Clicks
            # Calculate total clicks from individual channel columns
            filtered_data_copy = filtered_data.copy()
            filtered_data_copy['total_clicks'] = filtered_data_copy[['clicks_Facebook', 'clicks_Google', 'clicks_TikTok']].sum(axis=1)
            
            fig3 = px.scatter(filtered_data_copy.reset_index(), x='total_spend', y='total_clicks',
                            color='total_roas', size='total revenue',
                            title="Spend vs Clicks (colored by ROAS)")
            fig3.update_layout(xaxis_title="Total Spend ($)", yaxis_title="Total Clicks")
            st.plotly_chart(fig3, use_container_width=True)
        
        with col14:
            # Conversion Rate Analysis
            total_clicks_calculated = filtered_data[['clicks_Facebook', 'clicks_Google', 'clicks_TikTok']].sum().sum()
            conversion_rate = (filtered_data['# of orders'].sum() / total_clicks_calculated * 100) if total_clicks_calculated > 0 else 0
            fig4 = px.pie(values=[conversion_rate, 100-conversion_rate], 
                         names=['Converted', 'Not Converted'],
                         title=f"Overall Conversion Rate: {conversion_rate:.2f}%",
                         color_discrete_sequence=['#2ca02c', '#ff7f0e'])
            st.plotly_chart(fig4, use_container_width=True)

def create_channel_performance(combined_df, daily_marketing):
    """Create Channel Performance dashboard"""
    st.markdown('<div class="main-header">📱 Channel Performance</div>', unsafe_allow_html=True)
    
    # Channel comparison metrics
    channels = ['Facebook', 'Google', 'TikTok']
    
    # Aggregate data by channel
    channel_metrics = []
    for channel in channels:
        spend_col = f'spend_{channel}'
        revenue_col = f'attributed revenue_{channel}'
        roas_col = f'roas_{channel}'
        ctr_col = f'ctr_{channel}'
        cpc_col = f'cpc_{channel}'
        
        if spend_col in combined_df.columns:
            total_spend = combined_df[spend_col].sum()
            total_revenue = combined_df[revenue_col].sum()
            avg_roas = combined_df[roas_col].mean() if roas_col in combined_df.columns else 0
            avg_ctr = combined_df[ctr_col].mean() if ctr_col in combined_df.columns else 0
            avg_cpc = combined_df[cpc_col].mean() if cpc_col in combined_df.columns else 0
            
            channel_metrics.append({
                'Channel': channel,
                'Total Spend': total_spend,
                'Total Revenue': total_revenue,
                'Average ROAS': avg_roas,
                'Average CTR': avg_ctr,
                'Average CPC': avg_cpc
            })
    
    channel_df = pd.DataFrame(channel_metrics)
    
    if not channel_df.empty:
        # Channel comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            # ROAS by Channel - Pie Chart
            fig1 = px.pie(channel_df, values='Average ROAS', names='Channel',
                         title="ROAS Distribution by Channel",
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Spend vs Revenue by Channel
            fig2 = px.scatter(channel_df, x='Total Spend', y='Total Revenue',
                            size='Average ROAS', color='Channel',
                            title="Spend vs Revenue by Channel")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Time series by channel
        st.markdown("## 📊 Channel Performance Over Time")
        
        # ROAS trends by channel
        fig3 = px.line(daily_marketing, x='date', y='roas', color='channel',
                      title="ROAS Trends by Channel")
        fig3.update_layout(yaxis_title="ROAS")
        st.plotly_chart(fig3, use_container_width=True)
        
        # CTR and CPC comparison
        col3, col4 = st.columns(2)
        
        with col3:
            # CTR by Channel - Bar Chart
            fig_ctr = px.bar(channel_df, x='Channel', y='Average CTR',
                           title="Average CTR by Channel",
                           color='Average CTR',
                           color_continuous_scale='Blues')
            fig_ctr.update_layout(yaxis_title="CTR (%)")
            st.plotly_chart(fig_ctr, use_container_width=True)
        
        with col4:
            # CPC by Channel - Bar Chart
            fig_cpc = px.bar(channel_df, x='Channel', y='Average CPC',
                           title="Average CPC by Channel",
                           color='Average CPC',
                           color_continuous_scale='Reds')
            fig_cpc.update_layout(yaxis_title="CPC ($)")
            st.plotly_chart(fig_cpc, use_container_width=True)
        
        # Spend trends by channel
        fig4 = px.line(daily_marketing, x='date', y='spend', color='channel',
                      title="Spend Trends by Channel")
        fig4.update_layout(yaxis_title="Spend ($)")
        st.plotly_chart(fig4, use_container_width=True)
        
        # CTR and CPC trends over time
        col5, col6 = st.columns(2)
        
        with col5:
            fig_ctr_trend = px.line(daily_marketing, x='date', y='ctr', color='channel',
                                   title="CTR Trends by Channel")
            fig_ctr_trend.update_layout(yaxis_title="CTR (%)")
            st.plotly_chart(fig_ctr_trend, use_container_width=True)
        
        with col6:
            fig_cpc_trend = px.line(daily_marketing, x='date', y='cpc', color='channel',
                                   title="CPC Trends by Channel")
            fig_cpc_trend.update_layout(yaxis_title="CPC ($)")
            st.plotly_chart(fig_cpc_trend, use_container_width=True)
        
        # Channel metrics table
        st.markdown("## 📋 Channel Performance Summary")
        st.dataframe(channel_df.round(2), use_container_width=True)

def create_customer_acquisition(combined_df):
    """Create Customer Acquisition & Profitability dashboard"""
    st.markdown('<div class="main-header">👥 Customer Acquisition & Profitability</div>', unsafe_allow_html=True)
    
    # Date range selector
    date_range = st.date_input(
        "Select Date Range",
        value=(combined_df.index.min().date(), combined_df.index.max().date()),
        min_value=combined_df.index.min().date(),
        max_value=combined_df.index.max().date(),
        key="customer_date_range"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = combined_df[(combined_df.index.date >= start_date) & (combined_df.index.date <= end_date)]
        
        # Customer acquisition metrics
        col2, col3 = st.columns(2)
        
        
        with col2:
            fig2 = px.line(filtered_data.reset_index(), x='date', y='total_cac',
                          title="Total CAC Trend Over Time")
            fig2.update_layout(yaxis_title="CAC ($)")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            fig3 = px.line(filtered_data.reset_index(), x='date', y='gross_margin',
                          title="Gross Margin Trend Over Time")
            fig3.update_layout(yaxis_title="Gross Margin")
            st.plotly_chart(fig3, use_container_width=True)
        
        # AOV trend
        st.markdown("## 💰 Average Order Value Trend")
        fig4 = px.line(filtered_data.reset_index(), x='date', y='aov',
                      title="Average Order Value Over Time")
        fig4.update_layout(yaxis_title="AOV ($)")
        st.plotly_chart(fig4, use_container_width=True)
        
        # Profitability analysis
        st.markdown("## 📊 Profitability Analysis")
        
        # Gross margin vs spend
        fig5 = px.scatter(filtered_data.reset_index(), x='total_spend', y='gross_margin',
                         size='total revenue', color='total_roas',
                         title="Gross Margin vs Total Spend (colored by ROAS)")
        fig5.update_layout(xaxis_title="Total Spend ($)", yaxis_title="Gross Margin")
        st.plotly_chart(fig5, use_container_width=True)
        
        # Additional Customer Metrics
        st.markdown("## 👥 Customer Behavior Analysis")
        
        col7, col8 = st.columns(2)
        
        with col7:
            # Customer Acquisition Efficiency
            fig6 = px.scatter(filtered_data.reset_index(), x='new customers', y='total_cac',
                            color='total_roas', size='total revenue',
                            title="Customer Acquisition Efficiency")
            fig6.update_layout(xaxis_title="New Customers", yaxis_title="CAC ($)")
            st.plotly_chart(fig6, use_container_width=True)
        
        with col8:
            # Order Value Distribution
            fig7 = px.histogram(filtered_data.reset_index(), x='aov',
                               title="Average Order Value Distribution",
                               nbins=20)
            fig7.update_layout(xaxis_title="AOV ($)", yaxis_title="Frequency")
            st.plotly_chart(fig7, use_container_width=True)
        
        
        # Channel-specific Customer Acquisition
        st.markdown("## 📱 Channel-Specific Customer Metrics")
        
        channel_cac_data = []
        for channel in ['Facebook', 'Google', 'TikTok']:
            cac_col = f'cac_{channel}'
            spend_col = f'spend_{channel}'
            if cac_col in filtered_data.columns:
                avg_cac = filtered_data[cac_col].mean()
                total_spend = filtered_data[spend_col].sum()
                channel_cac_data.append({
                    'Channel': channel,
                    'Average CAC': avg_cac,
                    'Total Spend': total_spend
                })
        
        if channel_cac_data:
            channel_cac_df = pd.DataFrame(channel_cac_data)
            fig9 = px.bar(channel_cac_df, x='Channel', y='Average CAC',
                         title="Average CAC by Channel",
                         color='Average CAC',
                         color_continuous_scale='RdYlGn_r')
            fig9.update_layout(yaxis_title="CAC ($)")
            st.plotly_chart(fig9, use_container_width=True)

def create_campaign_analysis(marketing_df):
    """Create Campaign Analysis dashboard"""
    st.markdown('<div class="main-header">🎯 Campaign Analysis</div>', unsafe_allow_html=True)
    
    # Campaign filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_channels = st.multiselect("Select Channels", 
                                         options=marketing_df['channel'].unique(),
                                         default=marketing_df['channel'].unique())
    
    with col2:
        selected_tactics = st.multiselect("Select Tactics",
                                        options=marketing_df['tactic'].unique(),
                                        default=marketing_df['tactic'].unique())
    
    with col3:
        selected_states = st.multiselect("Select States",
                                       options=marketing_df['state'].unique(),
                                       default=marketing_df['state'].unique())
    
    # Filter data
    filtered_marketing = marketing_df[
        (marketing_df['channel'].isin(selected_channels)) &
        (marketing_df['tactic'].isin(selected_tactics)) &
        (marketing_df['state'].isin(selected_states))
    ]
    
    if not filtered_marketing.empty:
        # Campaign performance metrics
        campaign_performance = filtered_marketing.groupby(['campaign', 'channel', 'tactic']).agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'roas': 'mean',
            'ctr': 'mean',
            'cpc': 'mean',
            'cpm': 'mean'
        }).reset_index()
        
        campaign_performance = campaign_performance.sort_values('roas', ascending=False)
        
        # Top performing campaigns
        st.markdown("## 🏆 Top Performing Campaigns by ROAS")
        top_campaigns = campaign_performance.head(10)
        
        fig1 = px.bar(top_campaigns, x='campaign', y='roas', color='channel',
                     title="Top 10 Campaigns by ROAS")
        fig1.update_layout(xaxis_title="Campaign", yaxis_title="ROAS")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Campaign efficiency scatter plot
        fig2 = px.scatter(campaign_performance, x='spend', y='attributed revenue',
                         size='roas', color='channel',
                         title="Campaign Efficiency: Spend vs Revenue (sized by ROAS)")
        fig2.update_layout(xaxis_title="Total Spend ($)", yaxis_title="Attributed Revenue ($)")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed campaign table
        st.markdown("## 📋 Campaign Performance Details")
        st.dataframe(campaign_performance.round(2), use_container_width=True)

def main():
    """Main dashboard application"""
    # Load data
    combined_df, daily_marketing, marketing_df, business_df = load_data()
    
    if combined_df is None:
        st.stop()
    
    # Sidebar navigation
    st.sidebar.title("Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Select Dashboard View",
        ["Executive Overview", "Channel Performance", "Customer Acquisition", "Campaign Analysis"]
    )
    
    # Data info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Data Overview")
    st.sidebar.markdown(f"**Date Range:** {combined_df.index.min().strftime('%Y-%m-%d')} to {combined_df.index.max().strftime('%Y-%m-%d')}")
    st.sidebar.markdown(f"**Total Records:** {len(combined_df):,}")
    st.sidebar.markdown(f"**Channels:** Facebook, Google, TikTok")
    
    # Display selected page
    if page == "Executive Overview":
        create_executive_overview(combined_df)
    elif page == "Channel Performance":
        create_channel_performance(combined_df, daily_marketing)
    elif page == "Customer Acquisition":
        create_customer_acquisition(combined_df)
    elif page == "Campaign Analysis":
        create_campaign_analysis(marketing_df)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📝 Key Metrics Definitions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Marketing Metrics:**
        - **CTR (Click-Through Rate):** Clicks ÷ Impressions
        - **CPC (Cost Per Click):** Spend ÷ Clicks  
        - **CPM (Cost Per Mille):** (Spend ÷ Impressions) × 1000
        - **ROAS (Return on Ad Spend):** Attributed Revenue ÷ Spend
        """)
    
    with col2:
        st.markdown("""
        **Business Metrics:**
        - **AOV (Average Order Value):** Total Revenue ÷ # Orders
        - **CAC (Customer Acquisition Cost):** Spend ÷ New Customers
        - **Gross Margin:** Gross Profit ÷ Total Revenue
        """)

if __name__ == "__main__":
    main()
