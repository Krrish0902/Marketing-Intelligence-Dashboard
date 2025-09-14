# Marketing Intelligence Dashboard

A comprehensive Business Intelligence dashboard that connects marketing activity with business outcomes, built with Streamlit and Plotly.

## 🎯 Overview

This dashboard provides actionable insights by analyzing the relationship between marketing campaigns and business performance across three channels: Facebook, Google, and TikTok.

## 📊 Key Features

### Executive Overview
- **Top-level KPIs**: Total Spend, Revenue, Orders, ROAS, CAC, AOV
- **Trend Analysis**: Daily spend vs revenue correlation
- **Period-over-period comparisons** with percentage changes
- **Real-time metrics** with intuitive KPI cards

### Channel Performance
- **Channel comparison**: Facebook vs Google vs TikTok
- **ROAS analysis** by channel with visual comparisons
- **Spend efficiency** analysis (spend vs revenue scatter plots)
- **Time-series trends** for each channel
- **Performance summary table** with key metrics

### Customer Acquisition & Profitability
- **Customer acquisition cost (CAC)** trends and analysis
- **Gross margin** trends over time
- **Average Order Value (AOV)** analysis
- **Profitability correlation** with marketing spend
- **Customer acquisition efficiency** metrics

### Campaign Analysis
- **Campaign performance ranking** by ROAS
- **Campaign efficiency** analysis (spend vs revenue)
- **Filtering capabilities** by channel, tactic, and state
- **Detailed campaign metrics** table
- **Top performer identification**

## 🔧 Technical Architecture

### Data Processing Pipeline
- **Data Integration**: Combines marketing and business datasets
- **Metric Calculation**: Automated calculation of CTR, CPC, CPM, ROAS, AOV, CAC
- **Data Aggregation**: Daily, channel-level, and campaign-level aggregations
- **Data Validation**: Handles missing values and edge cases

### Dashboard Technology Stack
- **Frontend**: Streamlit for interactive web interface
- **Visualization**: Plotly for interactive charts and graphs
- **Data Processing**: Pandas for data manipulation and analysis
- **Caching**: Streamlit caching for optimal performance

## 📈 Key Metrics

### Marketing Metrics
- **CTR (Click-Through Rate)**: Clicks ÷ Impressions
- **CPC (Cost Per Click)**: Spend ÷ Clicks
- **CPM (Cost Per Mille)**: (Spend ÷ Impressions) × 1000
- **ROAS (Return on Ad Spend)**: Attributed Revenue ÷ Spend

### Business Metrics
- **AOV (Average Order Value)**: Total Revenue ÷ # Orders
- **CAC (Customer Acquisition Cost)**: Spend ÷ New Customers
- **Gross Margin**: Gross Profit ÷ Total Revenue

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Marketing-Intelligence-Dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Process the data**
```bash
python data_processing.py
```

4. **Run the dashboard**
```bash
streamlit run marketing_dashboard.py
```

5. **Access the dashboard**
Open your browser and navigate to `http://localhost:8501`

## 📁 Data Structure

### Input Files
- `business.csv`: Daily business metrics (orders, revenue, profit, COGS)
- `Facebook.csv`: Facebook campaign data
- `Google.csv`: Google campaign data  
- `TikTok.csv`: TikTok campaign data

### Generated Files
- `processed_combined.csv`: Combined business and marketing data
- `processed_daily_marketing.csv`: Daily marketing aggregations
- `processed_marketing.csv`: Individual campaign data with metrics
- `processed_business.csv`: Business data with calculated metrics


## 📊 Business Value

### For Marketing Teams
- **Channel Optimization**: Identify which channels drive the best ROAS and lowest CAC
- **Campaign Performance**: Track and compare campaign effectiveness
- **Budget Allocation**: Make data-driven decisions on spend distribution
- **Real-time Monitoring**: Track daily performance and trends

### For Business Stakeholders
- **Revenue Impact**: Understand how marketing spend correlates with business outcomes
- **Profitability Analysis**: Monitor gross margins and overall profitability
- **Customer Acquisition**: Track customer acquisition costs and efficiency
- **Strategic Planning**: Use insights for budget planning and growth strategies

### For Executives
- **KPI Dashboard**: High-level view of marketing ROI and business impact
- **Trend Analysis**: Identify patterns and opportunities for growth
- **Performance Tracking**: Monitor key metrics over time
- **Decision Support**: Data-driven insights for strategic decisions

## 🔄 Data Updates

### Automated Updates
To keep the dashboard current with new data:

1. **Update source files**: Replace CSV files with new data
2. **Re-run processing**: Execute `python data_processing.py`
3. **Refresh dashboard**: The dashboard will automatically reflect new data

### Scheduled Updates
For production environments, consider:
- **Automated data pipelines** to fetch new data
- **Scheduled processing** using cron jobs or task schedulers
- **API integrations** for real-time data updates

## 🛠️ Customization

### Adding New Metrics
1. **Update data_processing.py**: Add new metric calculations
2. **Modify dashboard.py**: Add new visualizations and KPIs
3. **Re-run processing**: Process data with new metrics

### Adding New Channels
1. **Update channel list** in data_processing.py
2. **Add channel-specific logic** in dashboard components
3. **Update filtering options** in the dashboard

### Styling Customization
- **CSS modifications**: Update the custom CSS in marketing_dashboard.py
- **Color schemes**: Modify Plotly color palettes
- **Layout changes**: Adjust Streamlit column layouts and spacing

## 📞 Support

For questions, issues, or feature requests:
- Check the documentation above
- Review the code comments for implementation details
- Create an issue in the repository for bugs or feature requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for data-driven marketing intelligence**