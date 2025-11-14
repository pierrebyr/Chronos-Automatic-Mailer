# API Keys Setup Guide

Complete guide to getting all the API keys you need for the Chronos Outreach System.

---

## Required APIs

### 1. ✅ Anthropic (Claude AI) - REQUIRED

**What it's used for:**
- Extracting brand information from websites
- Generating personalized cold emails
- Understanding web content

**Cost:** ~$0.03 per prospect (very cheap)

**How to get it:**

1. Go to: https://console.anthropic.com
2. Sign up or log in
3. Click "Get API Keys" or go to Settings
4. Click "Create Key"
5. Copy your key (starts with `sk-ant-`)

**Add to config.json:**
```json
{
    "anthropic_api_key": "sk-ant-YOUR-KEY-HERE"
}
```

---

### 2. 📧 Gmail API - REQUIRED FOR SENDING

You have two options:

#### Option A: Gmail API (Recommended - More Reliable)

**What it's used for:** Sending emails from your Gmail account

**How to get it:**

1. **Go to Google Cloud Console:**
   https://console.cloud.google.com

2. **Create a new project:**
   - Click "Select a project" → "New Project"
   - Name it "Chronos Outreach"
   - Click "Create"

3. **Enable Gmail API:**
   - In the left menu: "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click on it
   - Click "Enable"

4. **Create OAuth credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If asked, configure consent screen:
     * User Type: External
     * App name: "Chronos Outreach"
     * User support email: your email
     * Developer contact: your email
     * Click "Save and Continue" through the rest
   - Choose "Desktop app" as application type
   - Name it "Chronos Desktop"
   - Click "Create"

5. **Download credentials:**
   - Click the download button (⬇️) next to your new OAuth client
   - Save the file as `gmail_credentials.json`
   - Put it in the chronos_outreach folder

**First run authentication:**
- When you first run the system, it will open your browser
- Log in with your Gmail account
- Grant permissions
- Done! Token saved for future use

---

#### Option B: SMTP (Simpler but Less Reliable)

**What it's used for:** Sending emails via SMTP

**How to get it:**

1. **Create Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in if needed
   - Select app: "Mail"
   - Select device: "Other" → Name it "Chronos"
   - Click "Generate"
   - Copy the 16-character password (no spaces)

2. **Add to config.json:**
```json
{
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "pierre.bouyer@icloud.com",
        "password": "YOUR-16-CHAR-APP-PASSWORD"
    }
}
```

**Note:** If you use iCloud email, replace smtp.gmail.com with smtp.mail.me.com

---

### 3. 🔍 Brave Search API - OPTIONAL (Recommended)

**What it's used for:** Finding brands on the web

**Do you need it?** 
- NO - system works without it (uses DuckDuckGo fallback)
- YES - if you want better, faster search results

**Cost:** FREE up to 2,000 searches/month

**How to get it:**

1. **Go to:** https://brave.com/search/api/

2. **Sign up:**
   - Click "Get Started"
   - Create account
   - Verify email

3. **Get API key:**
   - Go to dashboard
   - Click "Get API Key"
   - Copy your key (starts with `BSA`)

**Add to config.json:**
```json
{
    "brave_api_key": "BSA-YOUR-KEY-HERE"
}
```

**Without Brave:**
The system will use DuckDuckGo HTML scraping as fallback. It works but is slower and less reliable.

---

## Complete config.json Example

```json
{
    "anthropic_api_key": "sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "brave_api_key": "BSAxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "sender_email": "pierre.bouyer@icloud.com",
    "database_path": "chronos_outreach.db",
    "gmail_credentials_path": "gmail_credentials.json"
}
```

Or with SMTP:

```json
{
    "anthropic_api_key": "sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "brave_api_key": "BSAxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "sender_email": "pierre.bouyer@icloud.com",
    "database_path": "chronos_outreach.db",
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "pierre.bouyer@icloud.com",
        "password": "abcd efgh ijkl mnop"
    }
}
```

---

## Quick Setup Using Setup Wizard

Instead of manually editing config.json, just run:

```bash
python setup.py setup
```

The wizard will:
1. Ask for each API key
2. Help you choose Gmail API or SMTP
3. Create config.json automatically
4. Tell you what to do next

---

## Testing Your Setup

After getting your API keys:

```bash
# Test everything
python setup.py test
```

This will verify:
- ✓ Anthropic API works
- ✓ Database connects
- ✓ Gmail is configured (doesn't send)

---

## Cost Summary

| API | Cost | Free Tier | Notes |
|-----|------|-----------|-------|
| **Anthropic** | ~$0.03/prospect | $5 credit | Required |
| **Brave Search** | FREE | 2,000/month | Optional |
| **Gmail API** | FREE | Unlimited* | Required |

*Within Gmail's sending limits (~500/day for personal accounts)

**Total cost for 100 prospects: ~$3.00**

---

## Troubleshooting

### "Invalid Anthropic API key"
- Make sure you copied the entire key (starts with `sk-ant-`)
- Check for extra spaces
- Verify it's not expired in the console

### "Gmail authentication failed"
- For Gmail API: Make sure `gmail_credentials.json` is in the folder
- For SMTP: Get a fresh App Password
- Try running `python email_sender.py` for detailed instructions

### "Brave Search not working"
- That's okay! System will use DuckDuckGo fallback
- Or get a free API key from https://brave.com/search/api/

### "Module not found"
```bash
pip install -r requirements.txt
```

---

## Security Best Practices

1. **Never commit config.json to Git**
   - It's already in .gitignore
   - Don't share it publicly

2. **Keep credentials private**
   - Don't share `gmail_credentials.json`
   - Don't share `gmail_token.pickle`

3. **Rotate keys if exposed**
   - Regenerate in API console
   - Update config.json

4. **Use environment variables in production**
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

---

## Ready to Go!

Once you have:
- ✅ Anthropic API key
- ✅ Gmail configured (API or SMTP)
- ✅ (Optional) Brave Search API key

Run:
```bash
python setup.py test
```

Then start using the system:
```bash
./chronos.sh  # or: python main.py research --category "Irish Whiskey"
```

---

**Need help?** Check the error messages - they're designed to tell you exactly what's wrong!
