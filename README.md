# Meta Campaign Management Automation

Automation tools for Meta (Facebook/Instagram) campaign management, budget control, and optimisation using the Facebook Business SDK.

## Features

- **Campaign CRUD Operations** - Create, read, update, delete campaigns programmatically
- **Budget Management** - Automated budget pacing and allocation based on performance
- **Performance analysis** - Real-time campaign performance retrieval with insights
- **Batch Operations** - Efficient bulk updates across multiple accounts
- **Error Handling** - Robust error handling and rate limit management
- **CLI Interface** - Simple command-line tools for common operations

---

## Prerequisites

### Required

- **Python 3.11+**
- **pip** (Python package manager)
- **Meta Business Account** with access to Ads Manager
- **Facebook Access Token** with `ads_read`, `ads_management` permissions
- **Business Account ID** (format: `ACT_1234567890`)

### Get Your Credentials

1. **Access Token**:
 - Go to [Meta Apps Dashboard](https://developers.facebook.com/apps/)
 - Create or select your app
 - Create a System User with Admin role
 - Generate a permanent token with `ads_read,ads_management` scopes
 - **Important**: System User tokens don't expire (user tokens expire after 60 days)

2. **Business Account ID**:
 - Go to [Meta Ads Manager](https://adsmanager.facebook.com/)
 - Settings → Business Settings
 - Find your Account ID (format: `ACT_...`)

### API Permissions Required

- `ads_read` - Read campaign data
- `ads_management` - Create, update, delete campaigns and budgets

---

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/gordongeraghty/meta-campaign-management.git
cd meta-campaign-management
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the repository root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
FACEBOOK_ACCESS_TOKEN=your_system_user_token_here
FACEBOOK_BUSINESS_ACCOUNT_ID=ACT_1234567890
```

### 5. Verify Installation

```bash
python scripts/list_campaigns.py --account-id ACT_1234567890
```

You should see a list of all campaigns with their IDs and budgets.

---

## Per-Script Usage Examples

### Script 1: `list_campaigns.py` - List All Campaigns

**Purpose**: Fetch and display all campaigns in your Meta Business Account with key metrics.

**Command**:

```bash
python scripts/list_campaigns.py --account-id ACT_1234567890
```

**Parameters**:

- `--account-id` (required): Your Meta Business Account ID (format: `ACT_xxx`)

**Example Output**:

```
================================================================================
CAMPAIGNS FOR ACCOUNT: ACT_1234567890
Total: 5 campaigns
================================================================================

ID: 123456789012345
Name: Q1_Brand_Awareness_Campaign
Status: ACTIVE
Objective: REACH
Daily Budget: $50.00
Created: 2024-01-15T10:30:00+0000
--------------------------------------------------------------------------------
ID: 123456789012346
Name: Q1_Conversions_Mobile
Status: PAUSED
Objective: CONVERSIONS
Daily Budget: $75.00
Created: 2024-01-20T14:22:00+0000
--------------------------------------------------------------------------------
```

**Expected Output**:

- Campaign ID (unique identifier)
- Campaign Name
- Status (ACTIVE, PAUSED, ARCHIVED, etc.)
- Objective (REACH, CONVERSIONS, etc.)
- Daily Budget (formatted as USD)
- Lifetime Budget (if applicable)
- Created timestamp

---

### Script 2: `create_campaign.py` - Create Campaigns from Config

**Purpose**: Bulk create campaigns from a JSON configuration file.

**Command**:

```bash
python scripts/create_campaign.py --account-id ACT_1234567890 --config campaigns.json
```

**Parameters**:

- `--account-id` (required): Your Meta Business Account ID
- `--config` (required): Path to JSON configuration file

**Configuration File Format** (`campaigns.json`):

```json
[
 {
 "name": "Q1_Brand_Awareness",
 "objective": "REACH",
 "daily_budget": 50.00,
 "status": "PAUSED"
 },
 {
 "name": "Q1_Conversions_Mobile",
 "objective": "CONVERSIONS",
 "daily_budget": 75.00,
 "status": "ACTIVE"
 },
 {
 "name": "Retargeting_Website_Visitors",
 "objective": "CONVERSIONS",
 "daily_budget": 30.00,
 "status": "PAUSED"
 }
]
```

**Configuration Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Campaign name (max 255 chars) |
| `objective` | string | Yes | Campaign objective (see [Campaign Objectives](#campaign-objectives)) |
| `daily_budget` | number | Yes | Daily budget in USD (e.g., 50.00 = $50) |
| `status` | string | No | Initial status: `ACTIVE` or `PAUSED` (default: `PAUSED`) |

**Campaign Objectives**:

- `REACH` - Maximize reach
- `IMPRESSIONS` - Maximize impressions
- `CONVERSIONS` - Drive conversions on website
- `SALES` - Drive sales on Facebook/Instagram
- `TRAFFIC` - Drive website traffic
- `ENGAGEMENT` - Maximize post engagement
- `LEAD_GENERATION` - Collect leads
- `APP_INSTALLS` - Drive app installs
- `VIDEO_VIEWS` - Maximize video views
- `STORE_VISITS` - Drive store visits

**Example Command**:

```bash
python scripts/create_campaign.py --account-id ACT_1234567890 --config campaigns.json
```

**Expected Output**:

```
- Created campaign 1: Q1_Brand_Awareness (ID: 123456789012347)
- Created campaign 2: Q1_Conversions_Mobile (ID: 123456789012348)
- Created campaign 3: Retargeting_Website_Visitors (ID: 123456789012349)

================================================================================
Summary: 3 created, 0 failed
================================================================================
```

---

### Script 3: `update_budget.py` - Update Budgets Based on Performance

**Purpose**: Scale campaign budgets based on recent performance metrics and ROAS.

**Command**:

```bash
python scripts/update_budget.py --account-id ACT_1234567890 --adjustment 10 --lookback 7
```

**Parameters**:

- `--account-id` (required): Your Meta Business Account ID
- `--adjustment` (optional): Budget adjustment percentage (default: 10, max: 50)
 - Positive values increase budget
 - Negative values decrease budget
 - Capped at 50% to prevent runaway changes
- `--lookback` (optional): Days of performance data to analyse (default: 7)

**Example Commands**:

```bash
# Increase budgets by 10% based on last 7 days performance
python scripts/update_budget.py --account-id ACT_1234567890 --adjustment 10 --lookback 7

# Decrease budgets by 5% based on last 14 days performance
python scripts/update_budget.py --account-id ACT_1234567890 --adjustment -5 --lookback 14

# Increase budgets by 20% based on last 3 days performance
python scripts/update_budget.py --account-id ACT_1234567890 --adjustment 20 --lookback 3
```

**Expected Output**:

```
Analyzing 5 campaigns (lookback: 7 days)

================================================================================
Campaign: Q1_Brand_Awareness_Campaign (ID: 123456789012345)
 Current Budget: $50.00
 Spend (last 7d): $320.45
 Conversions: 8
 CPA: $40.06
- Updated budget: $55.00 (+10%)
--------------------------------------------------------------------------------
Campaign: Q1_Conversions_Mobile (ID: 123456789012346)
 Current Budget: $75.00
 Spend (last 7d): $510.20
 Conversions: 15
 CPA: $34.01
- Updated budget: $82.50 (+10%)
--------------------------------------------------------------------------------
Campaign: Retargeting_Website_Visitors (ID: 123456789012349)
 No spend data (skipped)
--------------------------------------------------------------------------------

Summary: 2 campaigns updated, 0 errors
```

**Output Metrics**:

- **Current Budget**: Daily budget before adjustment
- **Spend**: Total spend in the lookback period
- **Conversions**: Number of conversion actions tracked
- **CPA**: Cost per acquisition (spend / conversions), shows "N/A" when no conversions
- **Updated Budget**: New daily budget after adjustment

---

## Configuration

### Environment Variables

Create `.env` file in repository root:

```env
# Required
FACEBOOK_ACCESS_TOKEN=your_system_user_token
FACEBOOK_BUSINESS_ACCOUNT_ID=ACT_1234567890

# Optional
LOG_LEVEL=INFO # DEBUG, INFO, WARNING, ERROR
```

### .env.example Template

```env
# Meta Business Credentials
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_BUSINESS_ACCOUNT_ID=ACT_your_account_id_here

# API Configuration
API_TIMEOUT=30
API_RETRIES=3

# Logging
LOG_LEVEL=INFO
```

---

## Security Best Practices

1. **Never commit `.env`** - Keep credentials out of version control
 ```bash
# Add to .gitignore
 .env
 .env.local
 *.key
 ```

2. **Use System Users** - Generate permanent tokens via Meta Business Manager
 - System User tokens don't expire
 - User Access Tokens expire after 60 days

3. **Rotate Credentials Regularly** - Regenerate tokens every 90 days

4. **Limit Permissions** - Use minimal scope required
 - Use `ads_read` for read-only operations
 - Use `ads_management` only when needed

5. **Implement Approval Chains** - Require review for large budget changes

6. **Add Budget Caps** - Prevent automation errors from costing money
 ```python
 MAX_DAILY_BUDGET = 1000 # $1000 cap per campaign
 MAX_ADJUSTMENT_PERCENT = 50 # Max 50% increase
 ```

---

## 🆘 Troubleshooting

### Error: `FACEBOOK_ACCESS_TOKEN not found in .env`

**Solution**: Ensure `.env` file exists in repository root with valid token:

```bash
# Create .env file
echo 'FACEBOOK_ACCESS_TOKEN=your_token' > .env
echo 'FACEBOOK_BUSINESS_ACCOUNT_ID=ACT_xxx' >> .env
```

### Error: `Invalid access token`

**Causes**:
- Token has expired
- Token was revoked
- Token doesn't have required permissions

**Solution**:
1. Go to [Meta Business Manager](https://business.facebook.com/)
2. System Users → Generate new token
3. Verify permissions include `ads_read` and `ads_management`
4. Update `.env` file

### Error: `(#10) This endpoint requires the 'ads_management' permission`

**Solution**: Your token lacks permissions. Regenerate with correct scope:
1. Business Manager → System Users
2. Select your System User
3. Remove existing token
4. Generate new token with `ads_management` scope

### Error: `Ads API rate limit exceeded`

**Solution**: The script includes exponential backoff, but you can:
1. Increase `--lookback` parameter to batch larger timeframes
2. Reduce number of campaigns processed
3. Run at off-peak times

### Error: `Campaign not found`

**Causes**:
- Campaign ID doesn't exist
- Campaign was archived/deleted
- Using wrong account ID

**Solution**:
```bash
# List campaigns to find valid IDs
python scripts/list_campaigns.py --account-id ACT_1234567890
```

---

## Links to Official Documentation

- **[Facebook Business SDK Documentation](https://developers.facebook.com/docs/business-sdk)** - Comprehensive SDK guide
- **[Marketing API Reference](https://developers.facebook.com/docs/marketing-api)** - Full API documentation
- **[Campaign API Documentation](https://developers.facebook.com/docs/marketing-api/reference/campaign)** - Campaign-specific docs
- **[Python SDK GitHub](https://github.com/facebook/facebook-python-business-sdk)** - Source code and examples
- **[Ads Manager Help](https://www.facebook.com/business/help/)** - Official Meta Ads help
- **[API Rate Limits](https://developers.facebook.com/docs/graph-api/overview/rate-limiting)** - Rate limiting details

---

## Related Repositories

- **[meta-creative-ai-generation](https://github.com/gordongeraghty/meta-creative-ai-generation)** - AI creative generation and bulk ad creation
- **[meta-competitor-intelligence](https://github.com/gordongeraghty/meta-competitor-intelligence)** - Competitor monitoring and creative analysis
- **[meta-ads-mcp-claude](https://github.com/gordongeraghty/meta-ads-mcp-claude)** - Claude AI integration for strategic recommendations
- **[n8n-meta-ads-workflows](https://github.com/gordongeraghty/n8n-meta-ads-workflows)** - n8n workflow automation
- **[empire-amplify-ads-automation](https://github.com/gordongeraghty/empire-amplify-ads-automation)** - Master hub with all repos

---

## Integration Examples

### n8n Workflow

Trigger this script daily via n8n:

```javascript
// n8n webhook to execute script
const { execSync } = require('child_process');
const result = execSync('python scripts/list_campaigns.py --account-id ACT_1234567890').toString();
return result;
```

### Google Workspace Integration

Log campaign data to Google Sheets via Zapier:

1. Create n8n workflow that runs `list_campaigns.py`
2. Connect to Zapier → Google Sheets
3. Append rows with campaign metrics

---

## License

MIT License - See LICENSE file

## Author

Gordon Geraghty - Head of Performance Media, Empire Amplify

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [Official Documentation](#-links-to-official-documentation)
3. Open a GitHub issue with detailed error message
