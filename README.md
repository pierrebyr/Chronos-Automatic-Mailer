# Chronos Studio - Automated Outreach System

A complete automated lead generation and cold outreach system for Chronos Studio. Research brands, generate personalized email sequences, and send them directly from your Gmail—all with a simple interface.

## Features

✅ **Automated Brand Research**
- Find brands in any category (e.g., "Irish Whiskey", "Premium Gin")
- Automatically scrape websites for contact information
- Extract products, descriptions, and company details

✅ **AI-Powered Email Generation**
- Personalized 3-email cold sequences using Claude AI
- Follows proven Chronos templates
- Customized for each brand's sector and products

✅ **Simple Review & Send Interface**
- Clean web interface to review all emails
- One-click sending or batch sending
- Track email status (sent/not sent)

✅ **Complete Database**
- SQLite database stores all prospects and emails
- Track status (prospect → contacted → lead → client)
- Add notes and manage relationships

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.json` with your API keys:

```json
{
    "anthropic_api_key": "sk-ant-...",
    "brave_api_key": "BSA...",  // Optional but recommended
    "sender_email": "pierre.bouyer@icloud.com"
}
```

**Get API Keys:**
- **Anthropic (Claude)**: https://console.anthropic.com
- **Brave Search** (optional): https://brave.com/search/api/

### 3. Set Up Gmail

#### Option A: Gmail API (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download and save as `gmail_credentials.json`

Run this for detailed instructions:
```bash
python email_sender.py
```

#### Option B: SMTP (Alternative)

Add to `config.json`:
```json
{
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "your-email@gmail.com",
        "password": "your-app-password"
    }
}
```

Get Gmail App Password: https://myaccount.google.com/apppasswords

### 4. First Run

Test your setup:
```bash
python main.py stats
```

## Usage

### Command Line Interface

The system has 5 main commands:

#### 1. Research Brands

Find and save brands in a category:

```bash
python main.py research --category "Irish Whiskey" --limit 20
```

This will:
- Search for brands in the category
- Find their websites
- Extract contact emails
- Save to database

**Examples:**
```bash
python main.py research --category "Premium Gin" --limit 15
python main.py research --category "Luxury Cosmetics" --limit 30
python main.py research --category "Craft Spirits" --limit 25
```

#### 2. Generate Email Sequences

Create personalized 3-email sequences:

```bash
# Generate for all prospects without emails
python main.py generate

# Generate for specific category
python main.py generate --category "Irish Whiskey"
```

#### 3. Review & Send (Web Interface)

Launch the interactive web interface:

```bash
python main.py review
```

This opens a Streamlit app where you can:
- View all prospects and their details
- Preview email sequences
- Send individual or batch emails
- Track what's been sent

#### 4. Send Emails (CLI)

Send emails directly from command line:

```bash
# Send email #1 to prospects with IDs 5, 8, and 12
python main.py send --prospects "5,8,12" --email 1

# Send email #2 to prospects 15, 16, 17
python main.py send --prospects "15,16,17" --email 2
```

#### 5. View Statistics

See system stats:

```bash
python main.py stats
```

Shows:
- Total prospects
- Prospects with email sequences
- Emails sent
- Categories tracked

## Complete Workflow

Here's the recommended workflow:

### Step 1: Research (5 minutes)

```bash
python main.py research --category "Premium Vodka" --limit 20
```

Wait while the system:
1. Searches for brands
2. Finds websites
3. Extracts contact info
4. Saves to database

### Step 2: Generate Emails (2 minutes)

```bash
python main.py generate
```

Claude AI creates personalized 3-email sequences for each prospect.

### Step 3: Review & Send (2 minutes)

```bash
python main.py review
```

In the web interface:
1. Go to "Email Sequences"
2. Review emails for each prospect
3. Edit if needed
4. Click "Send Email 1" for each

OR use batch sending:
1. Go to "Send Emails"
2. Select Email #1
3. Choose prospects
4. Click "SEND EMAILS"

### Step 4: Follow Up

After 7 days, send Email #2:
```bash
python main.py review
```

After 14 days, send Email #3.

## Web Interface Guide

### Dashboard
- View key metrics
- Quick access to main functions
- Research new categories

### Prospects
- Filter by category, status, or search
- View all prospect details
- Update prospect status
- Add notes

### Email Sequences
- View all 3 emails for each prospect
- Preview and edit before sending
- Send individual emails
- Track sent status

### Send Emails
- Batch send to multiple prospects
- Choose which email (#1, #2, or #3)
- Set delay between emails
- Preview before sending

## Database Structure

The system uses SQLite with 4 main tables:

1. **prospects**: Brand information and contact details
2. **email_sequences**: The 3 personalized emails for each prospect
3. **email_sends**: Tracking of sent emails
4. **notes**: Additional notes on prospects

Database file: `chronos_outreach.db`

## Email Templates

The system uses Chronos Studio's proven 3-email sequence:

**Email 1 - Introduction (Day 0)**
- Introduce Chronos Studio
- Highlight value proposition
- Offer demo/case studies

**Email 2 - Follow-up (Day 7)**
- Emphasize expertise + AI combination
- Mention similar clients
- Request 15-minute call

**Email 3 - Final (Day 14)**
- Brief reminder
- Create urgency with trial offer
- Easy opt-out

## Customization

### Modify Email Templates

Edit the prompts in `email_generator.py`:
- `_generate_email_1()`
- `_generate_email_2()`
- `_generate_email_3()`

### Change Chronos Info

Update `chronos_info` dictionary in `email_generator.py`:
```python
self.chronos_info = {
    'positioning': 'Your positioning',
    'key_benefits': ['Benefit 1', 'Benefit 2'],
    'clients': ['Client 1', 'Client 2'],
    ...
}
```

### Add Custom Fields

Extend the database schema in `database.py`:
```python
cursor.execute('''
    ALTER TABLE prospects 
    ADD COLUMN your_field TEXT
''')
```

## Troubleshooting

### "No search results found"
- Add Brave Search API key for better results
- Try different search queries
- Check internet connection

### "Could not find email"
- Some websites don't list emails publicly
- Manual verification may be needed
- Check contact pages manually

### "Gmail authentication failed"
- Ensure `gmail_credentials.json` is in the directory
- Re-run OAuth flow if token expired
- Use SMTP as fallback

### "Email generation failed"
- Check Anthropic API key
- Verify API rate limits
- Check error messages for details

## Best Practices

1. **Research in batches**: 20-30 brands at a time
2. **Review before sending**: Always preview emails
3. **Respect timing**: Wait 7 days between follow-ups
4. **Track responses**: Update prospect status when they reply
5. **Clean data**: Verify emails before batch sending
6. **Start small**: Test with 5-10 prospects first

## Rate Limits

- **Brave Search**: 1 request/second (free tier)
- **Claude API**: Depends on your plan
- **Gmail API**: 1-2 emails/second (to avoid spam flags)

The system includes delays to respect these limits.

## Project Structure

```
chronos_outreach/
├── main.py                 # Main orchestration
├── research_engine.py      # Brand research & scraping
├── email_generator.py      # AI email generation
├── database.py             # SQLite database
├── email_sender.py         # Gmail/SMTP sending
├── web_interface.py        # Streamlit UI
├── config.json             # Configuration
├── requirements.txt        # Dependencies
├── chronos_outreach.db     # SQLite database (created automatically)
├── gmail_credentials.json  # Gmail OAuth (you provide)
└── gmail_token.pickle      # Gmail token (created automatically)
```

## Security Notes

- Never commit `config.json` with real API keys
- Keep `gmail_credentials.json` and `gmail_token.pickle` private
- Use environment variables for production
- Don't share the database file (contains email addresses)

## Support

For issues or questions:
- Check error messages carefully
- Review configuration files
- Test with small batches first
- Verify API keys are valid

## License

Proprietary - Chronos Studio Internal Use Only

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Author**: Chronos Studio
