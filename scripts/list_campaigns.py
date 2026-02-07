#!/usr/bin/env python3
"""
List all campaigns in a Meta Business Account.

Usage:
    python scripts/list_campaigns.py --account-id ACT_1234567890
"""

import argparse
import os
import sys
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

load_dotenv()

def list_campaigns(account_id):
    """
    Fetch and display all campaigns with key metrics.

    Args:
        account_id (str): Meta Business Account ID (format: act_xxx)
    """
    try:
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            raise ValueError('FACEBOOK_ACCESS_TOKEN not found in .env')

        FacebookAdsApi.init(access_token=access_token)

        # Normalize account ID to lowercase act_ prefix
        if not account_id.lower().startswith('act_'):
            account_id = f'act_{account_id}'
        elif account_id.startswith('ACT_'):
            account_id = f'act_{account_id[4:]}'

        account = AdAccount(account_id)

        fields = [
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status,
            Campaign.Field.daily_budget,
            Campaign.Field.lifetime_budget,
            Campaign.Field.created_time,
            Campaign.Field.objective,
        ]

        campaigns = account.get_campaigns(fields=fields, params={'limit': 100})
        
        if not campaigns:
            print('No campaigns found for this account.')
            return
        
        print(f'\n{'='*80}')
        print(f'CAMPAIGNS FOR ACCOUNT: {account_id}')
        print(f'Total: {len(campaigns)} campaigns')
        print(f'{"="*80}\n')
        
        for campaign in campaigns:
            print(f"ID: {campaign['id']}")
            print(f"Name: {campaign['name']}")
            print(f"Status: {campaign['status']}")
            print(f"Objective: {campaign.get('objective', 'N/A')}")
            daily_budget = campaign.get('daily_budget')
            if daily_budget:
                print(f"Daily Budget: ${int(daily_budget) / 100:.2f}")
            lifetime_budget = campaign.get('lifetime_budget')
            if lifetime_budget:
                print(f"Lifetime Budget: ${int(lifetime_budget) / 100:.2f}")
            print(f"Created: {campaign.get('created_time', 'N/A')}")
            print('-' * 80)
        
        return campaigns
    
    except ValueError as e:
        print(f'Configuration Error: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error fetching campaigns: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List all campaigns in Meta Business Account')
    parser.add_argument('--account-id', required=True, help='Meta Business Account ID (format: ACT_xxx)')
    args = parser.parse_args()
    
    list_campaigns(args.account_id)
