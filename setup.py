#!/usr/bin/env python3
"""
Setup script for Chronos Outreach System
Run this to configure the system for first use
"""

import os
import json
import sys


def setup_wizard():
    """Interactive setup wizard"""
    print("\n" + "="*60)
    print("CHRONOS STUDIO - OUTREACH SYSTEM SETUP")
    print("="*60 + "\n")
    
    print("This wizard will help you configure the system.\n")
    
    # Check if config exists
    if os.path.exists('config.json'):
        response = input("config.json already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    config = {}
    
    # Anthropic API Key
    print("\n1. ANTHROPIC API KEY (Required)")
    print("   Get it from: https://console.anthropic.com")
    anthropic_key = input("   Enter your Anthropic API key: ").strip()
    
    if not anthropic_key:
        print("   ✗ Anthropic API key is required!")
        sys.exit(1)
    
    config['anthropic_api_key'] = anthropic_key
    
    # Brave Search API Key
    print("\n2. BRAVE SEARCH API KEY (Optional but recommended)")
    print("   Get it from: https://brave.com/search/api/")
    print("   Leave empty to skip (will use fallback search)")
    brave_key = input("   Enter your Brave Search API key (or press Enter): ").strip()
    
    config['brave_api_key'] = brave_key if brave_key else ""
    
    # Sender Information
    print("\n3. SENDER INFORMATION")
    sender_name = input("   Enter your name: ").strip()
    config['sender_name'] = sender_name if sender_name else "Your Name"

    sender_email = input("   Enter your email address: ").strip()
    config['sender_email'] = sender_email if sender_email else "your-email@example.com"

    sender_phone = input("   Enter your phone number: ").strip()
    config['sender_phone'] = sender_phone if sender_phone else "Your Phone Number"

    sender_website = input("   Enter your website (default: www.chronos.studio): ").strip()
    config['sender_website'] = sender_website if sender_website else "www.chronos.studio"

    # Email sending method
    print("\n4. EMAIL SENDING METHOD")
    print("   A) Gmail API (Recommended - more reliable)")
    print("   B) SMTP (Simpler setup)")
    
    method = input("   Choose method (A/B): ").strip().upper()
    
    if method == 'B':
        print("\n   SMTP Configuration:")
        smtp_host = input("   SMTP Host (default: smtp.gmail.com): ").strip() or "smtp.gmail.com"
        smtp_port = input("   SMTP Port (default: 587): ").strip() or "587"
        smtp_user = input("   SMTP Username (your email): ").strip()
        smtp_pass = input("   SMTP Password (App Password for Gmail): ").strip()
        
        config['smtp'] = {
            'host': smtp_host,
            'port': int(smtp_port),
            'username': smtp_user,
            'password': smtp_pass
        }
    else:
        print("\n   Gmail API selected.")
        print("   You'll need to:")
        print("   1. Download OAuth credentials from Google Cloud Console")
        print("   2. Save as 'gmail_credentials.json'")
        print("   3. Run the app - it will open browser for authentication")
        config['gmail_credentials_path'] = "gmail_credentials.json"
    
    # Database path
    config['database_path'] = "chronos_outreach.db"
    
    # Save config
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("\n" + "="*60)
    print("✓ Configuration saved to config.json")
    print("="*60)
    
    # Next steps
    print("\nNEXT STEPS:")
    print("\n1. If using Gmail API:")
    print("   - Get credentials from: https://console.cloud.google.com")
    print("   - Save as 'gmail_credentials.json'")
    print("   - Run: python email_sender.py (for detailed instructions)")
    
    print("\n2. Test your setup:")
    print("   python main.py stats")
    
    print("\n3. Start researching:")
    print("   python main.py research --category 'Irish Whiskey' --limit 10")
    
    print("\n4. Launch web interface:")
    print("   python main.py review")
    
    print("\n" + "="*60)
    print("Setup complete! 🎉")
    print("="*60 + "\n")


def test_setup():
    """Test the configuration"""
    print("\nTesting configuration...\n")
    
    # Check config file
    if not os.path.exists('config.json'):
        print("✗ config.json not found. Run setup first!")
        return False
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Check Anthropic key
    if not config.get('anthropic_api_key'):
        print("✗ Anthropic API key missing")
        return False
    print("✓ Anthropic API key found")
    
    # Test Anthropic connection
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=config['anthropic_api_key'])
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print("✓ Anthropic API working")
    except Exception as e:
        print(f"✗ Anthropic API error: {e}")
        return False
    
    # Check database
    try:
        from database import Database
        db = Database(config['database_path'])
        stats = db.get_statistics()
        print(f"✓ Database working ({stats['total_prospects']} prospects)")
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False
    
    print("\n✓ All tests passed!")
    return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chronos Outreach Setup')
    parser.add_argument('command', choices=['setup', 'test'], 
                       help='Run setup wizard or test configuration')
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        setup_wizard()
    elif args.command == 'test':
        test_setup()


if __name__ == '__main__':
    main()
