#!/usr/bin/env python3
"""
Update campaign budgets based on performance metrics.

Usage:
    python scripts/update_budget.py --account-id ACT_1234567890 --adjustment 10 --lookback 7
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.insights import AdsInsights

load_dotenv()

def update_budgets(account_id, adjustment_percent=10, lookback_days=7):
    """
    Scale campaign budgets based on recent ROAS performance.
    
    Args:
        account_id (str): Meta Business Account ID
        adjustment_percent (int): Percentage to adjust budgets (increase/decrease)
        lookback_days (int): Days of performance data to analyze
    """
    try:
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            raise ValueError('FACEBOOK_ACCESS_TOKEN not found in .env')
        
        FacebookAdsApi.init(access_token=access_token)
        
        # Fetch all active campaigns
        params = {
            'fields': ['id', 'name', 'daily_budget', 'status'],
            'limit': 100,
        }
        campaigns = Campaign.get_by_ids([account_id], params=params)
        
        date_start = (datetime.now() - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
        date_stop = datetime.now().strftime('%Y-%m-%d')
        
        updated = 0
        errors = 0
        
        print(f'\nAnalyzing {len(campaigns)} campaigns (lookback: {lookback_days} days)\n')
        print(f'{"="*80}')
        
        for campaign in campaigns:
            try:
                campaign_id = campaign['id']
                campaign_name = campaign['name']
                current_budget = int(campaign.get('daily_budget', 0)) / 100 if campaign.get('daily_budget') else 0
                
                # Get insights
                insights = campaign.get_insights(
                    fields=[AdsInsights.Field.spend, AdsInsights.Field.actions],
                    params={
                        'date_start': date_start,
                        'date_stop': date_stop,
                    }
                )
                
                if insights and len(insights) > 0:
                    insight = insights[0]
                    spend = float(insight.get('spend', 0))
                    conversions = len(insight.get('actions', []))
                    
                    if spend > 0:
                        cpa = spend / conversions if conversions > 0 else spend
                        print(f"Campaign: {campaign_name} (ID: {campaign_id})")
                        print(f"  Current Budget: ${current_budget:.2f}")
                        print(f"  Spend (last {lookback_days}d): ${spend:.2f}")
                        print(f"  Conversions: {conversions}")
                        print(f"  CPA: ${cpa:.2f}")
                        
                        # Apply adjustment
                        new_budget = int(current_budget * (100 + adjustment_percent) / 100 * 100)
                        campaign.update({Campaign.Field.daily_budget: new_budget})
                        new_budget_display = new_budget / 100
                        print(f"  ✓ Updated budget: ${new_budget_display:.2f} (+{adjustment_percent}%)")
                        updated += 1
                    else:
                        print(f"Campaign: {campaign_name} (ID: {campaign_id})")
                        print(f"  No spend data (skipped)")
                
                print('-' * 80)
            
            except Exception as e:
                print(f'Error updating campaign {campaign_id}: {str(e)}', file=sys.stderr)
                errors += 1
        
        print(f'\nSummary: {updated} campaigns updated, {errors} errors\n')
        return updated
    
    except ValueError as e:
        print(f'Configuration Error: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error updating budgets: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update campaign budgets based on performance')
    parser.add_argument('--account-id', required=True, help='Meta Business Account ID (format: ACT_xxx)')
    parser.add_argument('--adjustment', type=int, default=10, help='Budget adjustment percentage (default: 10)')
    parser.add_argument('--lookback', type=int, default=7, help='Days of performance data to analyze (default: 7)')
    args = parser.parse_args()
    
    update_budgets(args.account_id, args.adjustment, args.lookback)
