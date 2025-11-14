#!/usr/bin/env python3
"""
Email Sender Module - Send emails via Gmail API
"""

import base64
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle


class EmailSender:
    """Handles sending emails via Gmail API"""
    
    # Gmail API scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    def __init__(self, config):
        self.logger = logging.getLogger('chronos.email_sender')
        self.config = config
        self.service = None
        self.sender_email = config.get('sender_email', 'your-email@example.com')
        self.logger.info(f"Email Sender initialized with sender: {self.sender_email}")
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        token_path = 'gmail_token.pickle'
        credentials_path = self.config.get('gmail_credentials_path', 'gmail_credentials.json')
        
        # Load saved credentials if they exist
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Need to run OAuth flow
                if not os.path.exists(credentials_path):
                    print("\n⚠️  Gmail credentials not found!")
                    print("Please follow these steps:")
                    print("1. Go to Google Cloud Console: https://console.cloud.google.com")
                    print("2. Create a new project or select existing one")
                    print("3. Enable Gmail API")
                    print("4. Create OAuth 2.0 credentials (Desktop app)")
                    print("5. Download credentials and save as 'gmail_credentials.json'")
                    print("\nFor now, using SMTP fallback...\n")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=creds)
    
    def send_email(self, to_email, subject, body, html_body=None):
        """
        Send an email via Gmail API
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
            
        Returns:
            Boolean indicating success
        """
        if not self.service:
            # Fallback to SMTP if Gmail API not available
            return self._send_via_smtp(to_email, subject, body, html_body)
        
        try:
            # Create message
            if html_body:
                message = MIMEMultipart('alternative')
                message['To'] = to_email
                message['From'] = self.sender_email
                message['Subject'] = subject
                
                # Add plain text and HTML parts
                part1 = MIMEText(body, 'plain')
                part2 = MIMEText(html_body, 'html')
                message.attach(part1)
                message.attach(part2)
            else:
                message = MIMEText(body)
                message['To'] = to_email
                message['From'] = self.sender_email
                message['Subject'] = subject
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send via Gmail API
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return True
        
        except Exception as e:
            print(f"  ✗ Gmail API error: {e}")
            return False
    
    def _send_via_smtp(self, to_email, subject, body, html_body=None):
        """
        Fallback: Send email via SMTP
        
        Note: For production use, configure SMTP settings in config
        """
        import smtplib
        
        smtp_config = self.config.get('smtp', {})
        
        if not smtp_config:
            print("  ✗ No SMTP configuration available")
            print("  ℹ️  Email would be sent to:", to_email)
            print("  ℹ️  Subject:", subject)
            return False
        
        try:
            # Create message
            if html_body:
                message = MIMEMultipart('alternative')
                message['To'] = to_email
                message['From'] = self.sender_email
                message['Subject'] = subject
                
                part1 = MIMEText(body, 'plain')
                part2 = MIMEText(html_body, 'html')
                message.attach(part1)
                message.attach(part2)
            else:
                message = MIMEText(body)
                message['To'] = to_email
                message['From'] = self.sender_email
                message['Subject'] = subject
            
            # Send via SMTP
            server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(message)
            server.quit()
            
            return True
        
        except Exception as e:
            print(f"  ✗ SMTP error: {e}")
            return False
    
    def send_test_email(self, to_email):
        """Send a test email to verify configuration"""
        subject = "Test Email from Chronos Outreach System"
        body = """This is a test email from the Chronos Studio automated outreach system.

If you're receiving this, your email configuration is working correctly!

Best regards,
Chronos Outreach System"""
        
        html_body = """
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Test Email from Chronos Outreach System</h2>
            <p>This is a test email from the Chronos Studio automated outreach system.</p>
            <p>If you're receiving this, your email configuration is working correctly!</p>
            <p style="margin-top: 20px;">
                Best regards,<br>
                <strong>Chronos Outreach System</strong>
            </p>
        </body>
        </html>
        """
        
        success = self.send_email(to_email, subject, body, html_body)
        
        if success:
            print(f"✓ Test email sent successfully to {to_email}")
        else:
            print(f"✗ Failed to send test email to {to_email}")
        
        return success


def setup_gmail_api():
    """
    Helper function to set up Gmail API credentials
    Prints instructions for the user
    """
    print("\n" + "="*60)
    print("GMAIL API SETUP INSTRUCTIONS")
    print("="*60)
    print("""
To use Gmail API for sending emails, follow these steps:

1. Go to Google Cloud Console:
   https://console.cloud.google.com

2. Create a new project or select an existing one

3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the JSON file

5. Save the downloaded file as 'gmail_credentials.json' in the project directory

6. Run the application again - it will open a browser for authentication

Alternative: SMTP Configuration
===============================
If you prefer to use SMTP instead of Gmail API, add this to config.json:

{
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "your-email@gmail.com",
        "password": "your-app-password"
    }
}

Note: For Gmail SMTP, you need to create an "App Password":
https://myaccount.google.com/apppasswords
    """)
    print("="*60 + "\n")


if __name__ == '__main__':
    # Print setup instructions when run directly
    setup_gmail_api()
