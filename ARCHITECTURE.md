# System Architecture - Chronos Outreach System

Technical overview of how the automated outreach system works.

## Overview

The Chronos Outreach System is a Python-based automation pipeline that:
1. Researches brands using web search + AI
2. Generates personalized cold emails with Claude AI
3. Manages prospects in SQLite database
4. Sends emails via Gmail API or SMTP
5. Provides web UI for review and control

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  CLI Commands │  │ Web Interface │  │ Quick Launcher│     │
│  │  (main.py)   │  │ (Streamlit)   │  │ (chronos.sh) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │   ORCHESTRATION LAYER       │
              │   (ChronosOutreachSystem)   │
              └──────────────┬──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│  RESEARCH     │   │  EMAIL           │   │  DATABASE   │
│  ENGINE       │   │  GENERATOR       │   │  MANAGER    │
│               │   │                  │   │             │
│ - Web Search  │   │ - Claude AI      │   │ - SQLite    │
│ - Scraping    │   │ - Templates      │   │ - Tracking  │
│ - Extraction  │   │ - Personalize    │   │ - Status    │
└───────┬───────┘   └────────┬─────────┘   └──────┬──────┘
        │                    │                    │
        └────────────────────┴────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │   EMAIL SENDER              │
              │   - Gmail API               │
              │   - SMTP Fallback           │
              └─────────────────────────────┘
```

## Core Components

### 1. Main Orchestrator (`main.py`)

**Purpose**: Central coordinator for all operations

**Key Methods**:
- `research_category()`: Find and save brands
- `generate_email_sequences()`: Create personalized emails
- `send_email_batch()`: Send to multiple prospects
- `review_and_send()`: Launch web interface

**Flow**:
```
User Command → Main → Route to appropriate module → Execute → Return results
```

### 2. Research Engine (`research_engine.py`)

**Purpose**: Automated brand discovery and data enrichment

**Process**:
```
1. Web Search (Brave API or DuckDuckGo)
   ↓
2. Extract Brand Names (Claude AI)
   ↓
3. Find Official Websites
   ↓
4. Scrape Website Content
   ↓
5. Extract Contact Email
   ↓
6. Extract Products & Info (Claude AI)
   ↓
7. Save to Database
```

**Key Features**:
- Multiple search queries per category
- Duplicate detection
- Fallback search methods
- Email pattern matching (regex + common patterns)
- AI-powered information extraction

**Technologies**:
- `requests` for HTTP
- `BeautifulSoup` for HTML parsing
- `anthropic` for AI extraction
- Brave Search API or DuckDuckGo fallback

### 3. Email Generator (`email_generator.py`)

**Purpose**: Create personalized cold email sequences

**Process**:
```
Prospect Data → Claude AI Prompt → 3 Email Sequence → Save to DB
```

**Email Sequence**:
- **Email 1** (Day 0): Introduction + Value Prop
- **Email 2** (Day 7): Follow-up + Expertise
- **Email 3** (Day 14): Final touchpoint

**Personalization**:
- Company name and products
- Sector-specific messaging
- Dynamic client examples
- Custom value propositions

**AI Integration**:
- Uses Claude Sonnet 4.5
- Detailed prompts with Chronos info
- JSON response parsing
- Fallback templates if AI fails

### 4. Database (`database.py`)

**Purpose**: SQLite database for all data persistence

**Schema**:

```sql
prospects (
    id, name, company, email, website, 
    sector, category, products, description, 
    status, created_at, updated_at
)

email_sequences (
    id, prospect_id, email_number,
    subject, body, html_body, created_at
)

email_sends (
    id, prospect_id, email_number,
    sent_at, status
)

notes (
    id, prospect_id, note, created_at
)
```

**Key Operations**:
- CRUD for prospects
- Email sequence management
- Send tracking
- Status updates
- Statistics aggregation

### 5. Email Sender (`email_sender.py`)

**Purpose**: Send emails via Gmail

**Two Methods**:

**A. Gmail API** (Recommended):
```
OAuth Flow → Token → Gmail API → Send
```
- More reliable
- Better rate limits
- Requires OAuth setup

**B. SMTP** (Fallback):
```
SMTP Auth → TLS → Send
```
- Simpler setup
- Needs App Password
- Lower rate limits

**Features**:
- HTML + plain text support
- Error handling
- Test email function
- Automatic fallback

### 6. Web Interface (`web_interface.py`)

**Purpose**: Streamlit-based UI for review and control

**Pages**:

1. **Dashboard**:
   - Statistics overview
   - Quick actions
   - Research form

2. **Prospects**:
   - List all prospects
   - Filter and search
   - Update status
   - View details

3. **Email Sequences**:
   - Preview emails
   - Edit content
   - Send individually
   - Track status

4. **Send Emails**:
   - Batch selection
   - Email number choice
   - Send settings
   - Progress tracking

**Technology**: Streamlit (Python web framework)

## Data Flow

### Complete Workflow

```
1. USER INPUT
   └─> Category: "Irish Whiskey"
   └─> Limit: 20 brands

2. RESEARCH
   └─> Web Search → Find brands
   └─> For each brand:
       ├─> Find website
       ├─> Scrape content
       ├─> Extract email
       ├─> Extract info (AI)
       └─> Save to DB

3. GENERATE EMAILS
   └─> For each prospect:
       ├─> Load prospect data
       ├─> Generate Email 1 (AI)
       ├─> Generate Email 2 (AI)
       ├─> Generate Email 3 (AI)
       └─> Save to DB

4. REVIEW
   └─> Web UI displays:
       ├─> All prospects
       ├─> Email sequences
       └─> Send status

5. SEND
   └─> User selects prospects
   └─> System sends emails:
       ├─> With delays
       ├─> Tracks sends
       └─> Updates status
```

## API Integration

### Claude AI (Anthropic)

**Usage**:
- Extract brand names from search results
- Extract company info from websites
- Generate personalized emails

**Model**: `claude-sonnet-4-20250514`

**Prompt Strategy**:
- Detailed context
- Structured output (JSON)
- Fallback handling
- Error recovery

### Brave Search API (Optional)

**Usage**: Primary web search method

**Fallback**: DuckDuckGo HTML scraping

**Rate Limit**: 1 request/second (free tier)

### Gmail API

**Scopes**: `gmail.send`

**Auth Flow**:
1. OAuth credentials from Google Cloud
2. User consent (first run)
3. Token saved locally
4. Automatic refresh

## Configuration

### config.json

```json
{
    "anthropic_api_key": "sk-ant-...",
    "brave_api_key": "BSA...",
    "sender_email": "pierre.bouyer@icloud.com",
    "database_path": "chronos_outreach.db",
    "gmail_credentials_path": "gmail_credentials.json",
    "smtp": { ... }
}
```

### Security

- Config file in `.gitignore`
- Credentials never committed
- Token storage encrypted
- Database contains PII (protect accordingly)

## Error Handling

### Research Engine
- Retry on network errors
- Fallback search methods
- Skip invalid brands
- Continue on individual failures

### Email Generator
- Fallback templates
- JSON parsing with error recovery
- Continue if some fail

### Email Sender
- Graceful degradation to SMTP
- Rate limiting
- Send tracking
- Retry logic

## Performance

### Typical Timings

- **Research**: ~10 seconds per brand
  - Search: 1-2s
  - Scraping: 2-3s
  - Email finding: 3-5s
  - AI extraction: 2-3s

- **Email Generation**: ~10 seconds per prospect
  - 3 AI calls per prospect
  - ~3s per email

- **Sending**: ~2 seconds per email
  - Plus delay between sends (30s default)

### Optimization

- Parallel research (future)
- Caching search results
- Batch AI requests
- Database indexing

## Scalability

### Current Limits

- **Database**: SQLite (suitable for 10k+ prospects)
- **API Rate Limits**:
  - Brave: 1/sec
  - Claude: Varies by plan
  - Gmail: No hard limit (avoid spam)

### Future Enhancements

- PostgreSQL for larger scale
- Async operations (aiohttp)
- Parallel processing (multiprocessing)
- Cloud deployment
- Webhook integrations

## Testing

### Unit Tests (Future)

```python
test_research_engine.py
test_email_generator.py
test_database.py
test_email_sender.py
```

### Manual Testing

```bash
python setup.py test
python example.py test
```

## Deployment

### Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py setup
```

### Production (Future)

- Docker containerization
- Environment variables for config
- Scheduled cron jobs
- Monitoring and logging
- Backup automation

## Maintenance

### Regular Tasks

- Update API keys when expired
- Clean old database records
- Monitor send rates
- Update email templates
- Review AI prompts

### Monitoring

- Track success/failure rates
- Monitor API usage
- Check email delivery
- Review response rates

## Extensibility

### Adding New Features

**New Data Source**:
1. Create module in `research_engine.py`
2. Add to enrichment pipeline
3. Update database schema

**New Email Template**:
1. Edit `email_generator.py`
2. Update prompts
3. Test thoroughly

**New Sending Method**:
1. Add to `email_sender.py`
2. Implement interface
3. Add to config

## Troubleshooting

### Debug Mode

```python
# Add to any module
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **API Errors**: Check keys and rate limits
2. **Search Failures**: Use fallback or manual input
3. **Email Not Found**: Some sites hide contacts
4. **Send Failures**: Verify Gmail setup

## License

Proprietary - Chronos Studio Internal Use Only

---

**Version**: 1.0  
**Last Updated**: November 2025
