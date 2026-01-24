#!/usr/bin/env python3
"""
Create campaigns in Meta Business Account from JSON configuration.

Usage:
    python scripts/create_campaign.py --account-id ACT_1234567890 --config campaigns.json

Example campaigns.json:
    [
      {
        "name": "Q1_Brand_Awareness",
        "objective": "REACH",
        "daily_budget": 5000,
        "status": "PAUSED"
      }
    ]
"""

import argparse
import json
import os
import sys
import time
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign

load_dotenv()

def create_campaigns(account_id, config_file):
    """
    Create campaigns from JSON configuration file.
    
    Args:
        account_id (str): Meta Business Account ID
        config_file (str): Path to JSON config file with campaign definitions
    """
    try:
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            raise ValueError('FACEBOOK_ACCESS_TOKEN not found in .env')
        
        with open(config_file, 'r') as f:
            campaigns_config = json.load(f)
        
        if not isinstance(campaigns_config, list):
            raise ValueError('config_file must contain a JSON array of campaign objects')
        
        FacebookAdsApi.init(access_token=access_token)
        
        created_campaigns = []
        errors = []
        
        for idx, campaign_data in enumerate(campaigns_config, 1):
            try:
                # Convert daily_budget from cents to integer
                if 'daily_budget' in campaign_data:
                    campaign_data['daily_budget'] = int(campaign_data['daily_budget'] * 100)
                
                campaign = Campaign(account_id).create(campaign_data)
                created_campaigns.append(campaign)
                print(f"✓ Created campaign {idx}: {campaign_data.get('name')} (ID: {campaign['id']})")
                time.sleep(0.5)  # Rate limiting
            
            except Exception as e:
                error_msg = f"✗ Failed to create campaign {idx} ({campaign_data.get('name')}): {str(e)}"
                errors.append(error_msg)
                print(error_msg, file=sys.stderr)
        
        print(f'\n{"="*80}')
        print(f'Summary: {len(created_campaigns)} created, {len(errors)} failed')
        print(f'{"="*80}\n')
        
        if errors:
            sys.exit(1)
        
        return created_campaigns
    
    except FileNotFoundError:
        print(f'Error: Config file not found: {config_file}', file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON config: {e}', file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f'Configuration Error: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error creating campaigns: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create campaigns from JSON config')
    parser.add_argument('--account-id', required=True, help='Meta Business Account ID (format: ACT_xxx)')
    parser.add_argument('--config', required=True, help='Path to JSON configuration file')
    args = parser.parse_args()
    
    create_campaigns(args.account_id, args.config)
