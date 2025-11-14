#!/usr/bin/env python3
"""
Chronos Studio - Automated Lead Generation & Outreach System
Main orchestration module
"""

import os
import json
import anthropic
from datetime import datetime
from pathlib import Path

from research_engine import BrandResearcher
from email_generator import EmailSequenceGenerator
from database import Database
from email_sender import EmailSender


class ChronosOutreachSystem:
    """Main orchestration class for the automated outreach system"""
    
    def __init__(self, config_path="config.json"):
        self.config = self._load_config(config_path)
        self.db = Database(self.config['database_path'])
        self.researcher = BrandResearcher(self.config)
        self.email_gen = EmailSequenceGenerator(self.config)
        self.email_sender = EmailSender(self.config)
        
    def _load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def research_category(self, category, limit=20):
        """
        Research brands in a specific category
        
        Args:
            category: Category to research (e.g., "Irish Whiskey", "Premium Gin")
            limit: Maximum number of brands to find
            
        Returns:
            List of brand dictionaries
        """
        print(f"\n🔍 Researching brands in category: {category}")
        print(f"Target: {limit} brands\n")
        
        # Step 1: Find brands
        brands = self.researcher.find_brands(category, limit)
        print(f"✓ Found {len(brands)} brands")
        
        # Step 2: Enrich brand data (websites, contact info, products)
        enriched_brands = []
        for i, brand in enumerate(brands, 1):
            print(f"\n[{i}/{len(brands)}] Enriching: {brand['name']}")
            enriched = self.researcher.enrich_brand_data(brand)
            
            if enriched:
                enriched_brands.append(enriched)
                # Save to database immediately
                self.db.add_prospect(enriched, category)
                print(f"  ✓ Saved to database")
            else:
                print(f"  ✗ Could not enrich data")
        
        print(f"\n✓ Successfully enriched {len(enriched_brands)}/{len(brands)} brands")
        return enriched_brands
    
    def generate_email_sequences(self, category=None, prospect_ids=None):
        """
        Generate email sequences for prospects
        
        Args:
            category: Generate for all prospects in this category
            prospect_ids: Or generate for specific prospect IDs
        """
        if prospect_ids:
            prospects = [self.db.get_prospect(pid) for pid in prospect_ids]
        elif category:
            prospects = self.db.get_prospects_by_category(category)
        else:
            prospects = self.db.get_prospects_without_emails()
        
        print(f"\n✉️  Generating email sequences for {len(prospects)} prospects\n")
        
        for i, prospect in enumerate(prospects, 1):
            print(f"[{i}/{len(prospects)}] Generating for: {prospect['company']}")
            
            # Generate personalized email sequence
            email_sequence = self.email_gen.generate_sequence(prospect)
            
            # Save to database
            self.db.add_email_sequence(prospect['id'], email_sequence)
            print(f"  ✓ Saved 3 emails")
        
        print(f"\n✓ Generated email sequences for all prospects")
    
    def review_and_send(self):
        """
        Launch web interface for reviewing and sending emails
        """
        from web_interface import launch_app
        launch_app(self)
    
    def send_email_batch(self, prospect_ids, email_number=1, delay_seconds=30):
        """
        Send specific email from sequence to multiple prospects
        
        Args:
            prospect_ids: List of prospect IDs
            email_number: Which email in sequence (1, 2, or 3)
            delay_seconds: Delay between emails to avoid spam flags
        """
        print(f"\n📧 Sending email #{email_number} to {len(prospect_ids)} prospects\n")
        
        results = []
        for i, prospect_id in enumerate(prospect_ids, 1):
            prospect = self.db.get_prospect(prospect_id)
            email_data = self.db.get_email_sequence(prospect_id, email_number)
            
            print(f"[{i}/{len(prospect_ids)}] Sending to: {prospect['company']}")
            
            success = self.email_sender.send_email(
                to_email=prospect['email'],
                subject=email_data['subject'],
                body=email_data['body'],
                html_body=email_data.get('html_body')
            )
            
            if success:
                self.db.mark_email_sent(prospect_id, email_number)
                print(f"  ✓ Sent successfully")
                results.append({'prospect_id': prospect_id, 'success': True})
            else:
                print(f"  ✗ Failed to send")
                results.append({'prospect_id': prospect_id, 'success': False})
            
            # Delay between emails
            if i < len(prospect_ids):
                print(f"  ⏳ Waiting {delay_seconds}s...")
                import time
                time.sleep(delay_seconds)
        
        success_count = sum(1 for r in results if r['success'])
        print(f"\n✓ Sent {success_count}/{len(prospect_ids)} emails successfully")
        
        return results
    
    def get_statistics(self):
        """Get system statistics"""
        return self.db.get_statistics()


def main():
    """Main entry point with CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chronos Studio Automated Outreach System')
    parser.add_argument('command', choices=['research', 'generate', 'review', 'send', 'stats'],
                       help='Command to execute')
    parser.add_argument('--category', type=str, help='Product category (e.g., "Irish Whiskey")')
    parser.add_argument('--limit', type=int, default=20, help='Max brands to research')
    parser.add_argument('--email', type=int, choices=[1, 2, 3], default=1,
                       help='Email number in sequence')
    parser.add_argument('--prospects', type=str, help='Comma-separated prospect IDs')
    
    args = parser.parse_args()
    
    system = ChronosOutreachSystem()
    
    if args.command == 'research':
        if not args.category:
            print("Error: --category required for research command")
            return
        system.research_category(args.category, args.limit)
    
    elif args.command == 'generate':
        system.generate_email_sequences(category=args.category)
    
    elif args.command == 'review':
        system.review_and_send()
    
    elif args.command == 'send':
        if not args.prospects:
            print("Error: --prospects required for send command")
            return
        prospect_ids = [int(x.strip()) for x in args.prospects.split(',')]
        system.send_email_batch(prospect_ids, args.email)
    
    elif args.command == 'stats':
        stats = system.get_statistics()
        print("\n📊 CHRONOS OUTREACH STATISTICS")
        print("=" * 50)
        print(f"Total Prospects: {stats['total_prospects']}")
        print(f"With Email Sequences: {stats['with_sequences']}")
        print(f"Emails Sent: {stats['emails_sent']}")
        print(f"Categories: {', '.join(stats['categories'])}")
        print("=" * 50)


if __name__ == '__main__':
    main()
