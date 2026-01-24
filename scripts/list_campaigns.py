#!/usr/bin/env python3
"""
List all Meta campaigns with performance metrics.
Usage: python scripts/list_campaigns.py --account-id YOUR_ACCOUNT_ID
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.ad_account import AdAccount
import pandas as pd

load_dotenv()

# Initialize API
access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
if not access_token:
    print("ERROR: FACEBOOK_ACCESS_TOKEN not found in .env")
    sys.exit(1)

FacebookAdsApi.init(access_token=access_token)

def get_campaigns(account_id, limit=100):
    """
    Retrieve all campaigns for an ad account.
    """
    try:
        account = AdAccount(f'act_{account_id}')
        
        params = {
            'fields': [
                'id',
                'name',
                'status',
                'daily_budget',
                'lifetime_budget',
                'created_time',
                'objective',
                'buying_type',
            ],
            'limit': limit,
        }
        
        campaigns = account.get_campaigns(params=params)
        return list(campaigns)
        
    except Exception as e:
        print(f"ERROR: Failed to retrieve campaigns: {str(e)}")
        return []

def get_campaign_insights(campaign_id, lookback_days=7):
    """
    Get performance insights for a campaign.
    """
    try:
        campaign = Campaign(campaign_id)
        
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days)
        
        params = {
            'level': 'campaign',
            'fields': ['spend', 'impressions', 'clicks', 'actions'],
            'date_start': start_date.strftime('%Y-%m-%d'),
            'date_stop': end_date.strftime('%Y-%m-%d'),
        }
        
        insights = campaign.get_insights(params=params)
        return list(insights)
        
    except Exception as e:
        print(f"WARNING: Could not get insights for campaign {campaign_id}: {str(e)}")
        return []

def format_budget(budget_cents):
    """
    Convert budget from cents to dollars.
    """
    if budget_cents is None:
        return "N/A"
    return f"${budget_cents / 100:.2f}"

def main():
    parser = argparse.ArgumentParser(description='List Meta campaigns')
    parser.add_argument('--account-id', required=True, help='Ad Account ID')
    parser.add_argument('--limit', type=int, default=100, help='Number of campaigns to retrieve')
    parser.add_argument('--output', default='campaigns.csv', help='Output CSV file')
    parser.add_argument('--show-insights', action='store_true', help='Include performance insights')
    
    args = parser.parse_args()
    
    print(f"\n📊 Retrieving campaigns for account: {args.account_id}")
    print("="*80)
    
    # Get campaigns
    campaigns = get_campaigns(args.account_id, limit=args.limit)
    
    if not campaigns:
        print("No campaigns found.")
        return
    
    print(f"\n✅ Found {len(campaigns)} campaigns\n")
    
    # Prepare data
    campaign_data = []
    
    for campaign in campaigns:
        campaign_info = {
            'Campaign ID': campaign.get('id'),
            'Campaign Name': campaign.get('name'),
            'Status': campaign.get('status'),
            'Daily Budget': format_budget(campaign.get('daily_budget')),
            'Lifetime Budget': format_budget(campaign.get('lifetime_budget')),
            'Objective': campaign.get('objective'),
            'Buying Type': campaign.get('buying_type'),
            'Created': campaign.get('created_time'),
        }
        
        # Add insights if requested
        if args.show_insights:
            insights = get_campaign_insights(campaign.get('id'))
            if insights:
                insight = insights[0]
                campaign_info['Spend (7d)'] = f"${float(insight.get('spend', 0)):.2f}"
                campaign_info['Impressions (7d)'] = insight.get('impressions', 0)
                campaign_info['Clicks (7d)'] = insight.get('clicks', 0)
        
        campaign_data.append(campaign_info)
    
    # Create DataFrame
    df = pd.DataFrame(campaign_data)
    
    # Print to console
    print(df.to_string(index=False))
    
    # Export to CSV
    df.to_csv(args.output, index=False)
    print(f"\n💾 Exported to: {args.output}")
    
    # Summary statistics
    print(f"\n📈 Summary:")
    print(f"  Total Campaigns: {len(campaigns)}")
    active_count = len([c for c in campaigns if c.get('status') == 'ACTIVE'])
    paused_count = len([c for c in campaigns if c.get('status') == 'PAUSED'])
    print(f"  Active: {active_count}")
    print(f"  Paused: {paused_count}")

if __name__ == '__main__':
    main()
