# Meta Campaign Management Automation

Automation tools for Meta (Facebook/Instagram) campaign management, budget control, and optimization using the Facebook Business SDK.

## 🎯 Features

- **Campaign CRUD Operations** - Create, read, update, delete campaigns programmatically
- **Budget Management** - Automated budget pacing and allocation
- **Ad Set Optimization** - Performance-based ad set management
- **Quality Control** - Naming convention enforcement and structure audits
- **Batch Operations** - Efficient bulk updates across multiple accounts
- **Performance Metrics** - Real-time campaign performance retrieval

## 🚀 Quick Start

### Installation

```bash
pip install facebook_business
pip install python-dotenv
```

### Authentication

1. Create a `.env` file:

```env
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_BUSINESS_ACCOUNT_ID=your_business_account_id
```

2. Use System Users in Meta Business Manager for permanent tokens (avoids 60-day expiration)

### Basic Usage

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
business_account_id = os.getenv('FACEBOOK_BUSINESS_ACCOUNT_ID')

FacebookAdsApi.init(access_token=access_token)

params = {
    'fields': ['id', 'name', 'status', 'daily_budget', 'created_time'],
    'limit': 100,
}

campaigns = Campaign.get_by_ids([business_account_id], params=params)

for campaign in campaigns:
    print(f"Campaign: {campaign['name']} (ID: {campaign['id']})")
    print(f"Daily Budget: {campaign.get('daily_budget', 'N/A')}")
    print(f"Status: {campaign['status']}")
    print("---")
```

## 📁 Repository Structure

```
meta-campaign-management/
├── scripts/
│   ├── create_campaigns.py
│   ├── list_campaigns.py
│   ├── update_budget.py
│   ├── pause_underperformers.py
│   ├── bulk_operations.py
│   └── naming_convention_check.py
├── config/
│   ├── settings.py
│   └── .env.example
├── utils/
│   ├── api_handler.py
│   ├── error_handler.py
│   └── rate_limiter.py
├── requirements.txt
└── README.md
```

## 🔑 Key Scripts

### 1. List All Campaigns

```bash
python scripts/list_campaigns.py --account-id YOUR_BUSINESS_ACCOUNT_ID
```

Retrieve all campaigns with key metrics:
- Campaign ID
- Campaign Name
- Daily Budget
- Status (ACTIVE/PAUSED)
- Created Date

### 2. Create Campaigns

```bash
python scripts/create_campaigns.py --file campaigns.json
```

Bulk create campaigns from JSON:

```json
[
  {
    "name": "Q1_Brand_Awareness",
    "objective": "REACH",
    "daily_budget": 50000,
    "status": "PAUSED"
  },
  {
    "name": "Q1_Conversions_Mobile",
    "objective": "CONVERSIONS",
    "daily_budget": 75000,
    "status": "PAUSED"
  }
]
```

### 3. Naming Convention Check

```bash
python scripts/naming_convention_check.py --pattern '[Format]_[Topic]_[CTA]_[Version]'
```

Enforces consistent naming:
- ✅ Correct: `Video_Spring_ShopNow_V1`
- ❌ Wrong: `spring campaign v1`

### 4. Budget Automation

```bash
python scripts/update_budget.py --adjustment 10 --min-threshold 0.5 --max-threshold 2.0
```

Automates budget allocation:
- Scale winners by 10%
- Pause underperformers (ROAS < 0.5)
- Cap daily budget changes (max 2.0x adjustment)

### 5. Pause Underperformers

```bash
python scripts/pause_underperformers.py --min-cpa 50 --min-ctr 0.015 --lookback 3
```

Automatically pause ads that don't meet thresholds over last 3 days:
- CPA > $50
- CTR < 1.5%

## ⚙️ API Rate Limiting

Meta's API enforces rolling 1-hour rate limits. This tool includes exponential backoff:

```python
# Automatic retry with exponential backoff
for attempt in range(5):
    try:
        result = api_call()
        break
    except RateLimitException:
        wait_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
        time.sleep(wait_time)
```

## 🔐 Security Best Practices

1. **Never commit `.env`** - Use `.env.example` for reference
2. **Use System Users** - Generate permanent tokens in Meta Business Manager
3. **Store tokens securely** - Use environment variables or secret managers
4. **Implement approval chains** - Require review before large budget changes
5. **Add maximum spend caps** - Prevent automation errors from costing clients money

## 📊 Integration with Empire Amplify Stack

- **n8n Pro**: Trigger scripts via webhooks on schedule
- **Zapier Max**: Route campaign alerts to Slack/Email
- **Gemini Enterprise**: AI analysis of campaign performance
- **Google Sheets**: Log campaign data for tracking

## 🤝 Related Repositories

- [meta-creative-ai-generation](https://github.com/gordongeraghty/meta-creative-ai-generation) - AI creative generation
- [meta-competitor-intelligence](https://github.com/gordongeraghty/meta-competitor-intelligence) - Competitor monitoring
- [n8n-meta-ads-workflows](https://github.com/gordongeraghty/n8n-meta-ads-workflows) - n8n workflow templates
- [empire-amplify-ads-automation](https://github.com/gordongeraghty/empire-amplify-ads-automation) - Master hub

## 📚 Resources

- [Facebook Business SDK Docs](https://developers.facebook.com/docs/business-sdk)
- [Marketing API Reference](https://developers.facebook.com/docs/marketing-api)
- [Python SDK on GitHub](https://github.com/facebook/facebook-python-business-sdk)
- [Meta Ads Best Practices](https://www.facebook.com/business/help/)

## 📝 License

MIT License - See LICENSE file

## 👥 Author

Gordon Geraghty - Head of Performance Media, Empire Amplify
