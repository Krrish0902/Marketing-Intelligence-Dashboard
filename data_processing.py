import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_process_data():
    """
    Load and process all marketing and business datasets
    """
    print("Loading datasets...")
    
    # Load business data
    business_df = pd.read_csv('business.csv')
    business_df['date'] = pd.to_datetime(business_df['date'])
    
    # Load marketing data
    facebook_df = pd.read_csv('Facebook.csv')
    google_df = pd.read_csv('Google.csv')
    tiktok_df = pd.read_csv('TikTok.csv')
    
    # Add channel column to each marketing dataset
    facebook_df['channel'] = 'Facebook'
    google_df['channel'] = 'Google'
    tiktok_df['channel'] = 'TikTok'
    
    # Standardize column names (fix impression column name)
    facebook_df = facebook_df.rename(columns={'impression': 'impressions'})
    google_df = google_df.rename(columns={'impression': 'impressions'})
    tiktok_df = tiktok_df.rename(columns={'impression': 'impressions'})
    
    # Convert dates
    for df in [facebook_df, google_df, tiktok_df]:
        df['date'] = pd.to_datetime(df['date'])
    
    # Combine marketing data
    marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
    
    print(f"Loaded {len(business_df)} business records")
    print(f"Loaded {len(marketing_df)} marketing records")
    
    return business_df, marketing_df

def calculate_marketing_metrics(marketing_df):
    """
    Calculate derived marketing metrics
    """
    print("Calculating marketing metrics...")
    
    # Calculate derived metrics
    marketing_df['ctr'] = marketing_df['clicks'] / marketing_df['impressions']
    marketing_df['cpc'] = marketing_df['spend'] / marketing_df['clicks']
    marketing_df['cpm'] = (marketing_df['spend'] / marketing_df['impressions']) * 1000
    marketing_df['roas'] = marketing_df['attributed revenue'] / marketing_df['spend']
    
    # Handle division by zero
    marketing_df['ctr'] = marketing_df['ctr'].fillna(0)
    marketing_df['cpc'] = marketing_df['cpc'].fillna(0)
    marketing_df['cpm'] = marketing_df['cpm'].fillna(0)
    marketing_df['roas'] = marketing_df['roas'].fillna(0)
    
    return marketing_df

def calculate_business_metrics(business_df):
    """
    Calculate derived business metrics
    """
    print("Calculating business metrics...")
    
    # Calculate derived metrics
    business_df['gross_margin'] = business_df['gross profit'] / business_df['total revenue']
    business_df['aov'] = business_df['total revenue'] / business_df['# of orders']
    
    # Handle division by zero
    business_df['gross_margin'] = business_df['gross_margin'].fillna(0)
    business_df['aov'] = business_df['aov'].fillna(0)
    
    return business_df

def create_combined_dataset(business_df, marketing_df):
    """
    Combine business and marketing data for analysis
    """
    print("Creating combined dataset...")
    
    # Aggregate marketing data by date and channel
    daily_marketing = marketing_df.groupby(['date', 'channel']).agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum',
        'attributed revenue': 'sum',
        'ctr': 'mean',
        'cpc': 'mean',
        'cpm': 'mean',
        'roas': 'mean'
    }).reset_index()
    
    # Create separate columns for each channel
    channels = ['Facebook', 'Google', 'TikTok']
    marketing_data = {}
    
    for channel in channels:
        channel_data = daily_marketing[daily_marketing['channel'] == channel].set_index('date')
        for col in ['impressions', 'clicks', 'spend', 'attributed revenue', 'ctr', 'cpc', 'cpm', 'roas']:
            if col in channel_data.columns:
                marketing_data[f'{col}_{channel}'] = channel_data[col]
    
    # Create DataFrame from marketing data
    marketing_pivot = pd.DataFrame(marketing_data)
    
    # Merge with business data
    combined_df = business_df.set_index('date').join(marketing_pivot, how='outer').fillna(0)
    
    # Calculate CAC (Customer Acquisition Cost) for each channel
    for channel in channels:
        spend_col = f'spend_{channel}'
        new_customers_col = 'new customers'
        if spend_col in combined_df.columns:
            combined_df[f'cac_{channel}'] = np.where(
                combined_df[new_customers_col] > 0,
                combined_df[spend_col] / combined_df[new_customers_col],
                0
            )
    
    # Calculate total marketing metrics
    spend_cols = [f'spend_{channel}' for channel in channels if f'spend_{channel}' in combined_df.columns]
    revenue_cols = [f'attributed revenue_{channel}' for channel in channels if f'attributed revenue_{channel}' in combined_df.columns]
    
    combined_df['total_spend'] = combined_df[spend_cols].sum(axis=1)
    combined_df['total_attributed_revenue'] = combined_df[revenue_cols].sum(axis=1)
    combined_df['total_roas'] = np.where(
        combined_df['total_spend'] > 0,
        combined_df['total_attributed_revenue'] / combined_df['total_spend'],
        0
    )
    combined_df['total_cac'] = np.where(
        combined_df['new customers'] > 0,
        combined_df['total_spend'] / combined_df['new customers'],
        0
    )
    
    return combined_df, daily_marketing

def process_all_data():
    """
    Main function to process all data
    """
    print("Starting data processing...")
    
    # Load and process data
    business_df, marketing_df = load_and_process_data()
    
    # Calculate metrics
    marketing_df = calculate_marketing_metrics(marketing_df)
    business_df = calculate_business_metrics(business_df)
    
    # Create combined dataset
    combined_df, daily_marketing = create_combined_dataset(business_df, marketing_df)
    
    print("Data processing completed!")
    print(f"Combined dataset shape: {combined_df.shape}")
    print(f"Daily marketing data shape: {daily_marketing.shape}")
    
    return business_df, marketing_df, combined_df, daily_marketing

if __name__ == "__main__":
    # Process data when script is run directly
    business_df, marketing_df, combined_df, daily_marketing = process_all_data()
    
    # Save processed data
    business_df.to_csv('processed_business.csv', index=False)
    marketing_df.to_csv('processed_marketing.csv', index=False)
    combined_df.to_csv('processed_combined.csv')
    daily_marketing.to_csv('processed_daily_marketing.csv', index=False)
    
    print("Processed data saved to CSV files")
