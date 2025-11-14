# Quick Start Guide - Chronos Outreach System

Get up and running in 5 minutes!

## 1. Install (1 minute)

```bash
# Clone or download the project
cd chronos_outreach

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configure (2 minutes)

Run the setup wizard:

```bash
python setup.py setup
```

You'll need:
- **Anthropic API key** (get from https://console.anthropic.com)
- **Email** (your Gmail address)
- **Brave Search API key** (optional - get from https://brave.com/search/api/)

For Gmail sending, choose:
- **Option A**: Gmail API (recommended) - requires OAuth setup
- **Option B**: SMTP - needs App Password

## 3. Use It (2 minutes)

### Quick Launcher

**Mac/Linux:**
```bash
./chronos.sh
```

**Windows:**
```bash
chronos.bat
```

**Or use directly:**

```bash
# Research brands
python main.py research --category "Irish Whiskey" --limit 10

# Generate emails
python main.py generate

# Launch web interface
python main.py review
```

## Complete Workflow

### Step 1: Research (2 min)
```bash
python main.py research --category "Premium Vodka" --limit 20
```

System finds brands, websites, emails, products automatically.

### Step 2: Generate Emails (1 min)
```bash
python main.py generate
```

AI creates personalized 3-email sequences for each brand.

### Step 3: Review & Send (2 min)
```bash
python main.py review
```

Web interface opens:
1. Review emails
2. Edit if needed
3. Send individually or in batch

Done! 🎉

## Gmail Setup (Optional)

### Gmail API (Recommended)

1. Go to https://console.cloud.google.com
2. Create project → Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download as `gmail_credentials.json`
5. Run app - it will authenticate

### SMTP (Simpler)

1. Get App Password: https://myaccount.google.com/apppasswords
2. Add to config.json:

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

## Example Commands

```bash
# Research different categories
python main.py research --category "Craft Gin" --limit 15
python main.py research --category "Luxury Cosmetics" --limit 25

# View stats
python main.py stats

# Send emails to specific prospects
python main.py send --prospects "1,2,3" --email 1

# Test setup
python setup.py test

# Run examples
python example.py
python example.py test
python example.py demo-research
```

## Tips

- Start with 10 brands to test the system
- Always review emails before sending
- Wait 7 days between Email #1 and #2
- Track responses in the web interface
- Use batch sending for efficiency

## Troubleshooting

**"No API key"**
→ Run: `python setup.py setup`

**"Can't find emails"**
→ Some sites hide emails - manual check may be needed

**"Gmail auth failed"**
→ Get credentials from Google Cloud Console

**"Search not working"**
→ Add Brave Search API key (optional)

## Need Help?

1. Check `README.md` for detailed docs
2. Run `python example.py` for examples
3. Test with `python setup.py test`

---

That's it! You're ready to automate your outreach. 🚀
