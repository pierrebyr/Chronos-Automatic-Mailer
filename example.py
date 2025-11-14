#!/usr/bin/env python3
"""
Example Usage Script
Demonstrates a complete workflow with the Chronos Outreach System
"""

from main import ChronosOutreachSystem


def example_workflow():
    """
    Complete example workflow:
    1. Research brands in a category
    2. Generate email sequences
    3. Review and send
    """
    
    print("\n" + "="*60)
    print("CHRONOS OUTREACH SYSTEM - EXAMPLE WORKFLOW")
    print("="*60 + "\n")
    
    # Initialize system
    system = ChronosOutreachSystem()
    
    # Example 1: Research Irish Whiskey brands
    print("\n📝 EXAMPLE 1: Research Brands")
    print("-" * 60)
    
    category = "Irish Whiskey"
    print(f"\nResearching {category} brands...")
    print("This will find brands, websites, and contact info.\n")
    
    # Uncomment to actually run:
    # brands = system.research_category(category, limit=5)
    # print(f"✓ Found {len(brands)} brands")
    
    print("💡 To run: system.research_category('Irish Whiskey', limit=5)")
    
    # Example 2: Generate email sequences
    print("\n\n📧 EXAMPLE 2: Generate Email Sequences")
    print("-" * 60)
    
    print("\nGenerating personalized email sequences...")
    print("This creates 3 emails for each prospect.\n")
    
    # Uncomment to actually run:
    # system.generate_email_sequences(category=category)
    # print("✓ Email sequences generated")
    
    print("💡 To run: system.generate_email_sequences()")
    
    # Example 3: View statistics
    print("\n\n📊 EXAMPLE 3: View Statistics")
    print("-" * 60)
    
    stats = system.get_statistics()
    
    print(f"\nTotal Prospects: {stats['total_prospects']}")
    print(f"With Email Sequences: {stats['with_sequences']}")
    print(f"Emails Sent: {stats['emails_sent']}")
    print(f"Categories: {', '.join(stats['categories']) if stats['categories'] else 'None'}")
    
    # Example 4: Send emails (batch)
    print("\n\n📤 EXAMPLE 4: Send Emails")
    print("-" * 60)
    
    print("\nTo send emails to prospects with IDs 1, 2, 3:")
    print("system.send_email_batch([1, 2, 3], email_number=1)")
    
    # Uncomment to actually run:
    # results = system.send_email_batch([1, 2, 3], email_number=1, delay_seconds=30)
    
    print("\n💡 Or use the web interface: python main.py review")
    
    # Example 5: Launch web interface
    print("\n\n🌐 EXAMPLE 5: Launch Web Interface")
    print("-" * 60)
    
    print("\nThe web interface provides:")
    print("• Dashboard with statistics")
    print("• Prospect management")
    print("• Email preview and editing")
    print("• Batch sending with controls")
    
    print("\n💡 To launch: python main.py review")
    
    print("\n" + "="*60)
    print("END OF EXAMPLES")
    print("="*60 + "\n")


def quick_test():
    """Quick test of basic functionality"""
    print("\n🧪 QUICK TEST\n")
    
    system = ChronosOutreachSystem()
    
    # Test 1: Database connection
    try:
        stats = system.get_statistics()
        print("✓ Database connected")
        print(f"  Current prospects: {stats['total_prospects']}")
    except Exception as e:
        print(f"✗ Database error: {e}")
        return
    
    # Test 2: AI connection
    try:
        from email_generator import EmailSequenceGenerator
        gen = EmailSequenceGenerator(system.config)
        print("✓ AI (Claude) connected")
    except Exception as e:
        print(f"✗ AI connection error: {e}")
        return
    
    print("\n✓ All systems operational!\n")


def demo_research():
    """Demo the research functionality with a small example"""
    print("\n🔬 DEMO: Research Functionality\n")
    
    system = ChronosOutreachSystem()
    
    print("Let's research a few Premium Gin brands...")
    print("(This will take about 2-3 minutes)\n")
    
    response = input("Continue with demo? (y/n): ")
    
    if response.lower() == 'y':
        brands = system.research_category("Premium Gin", limit=3)
        
        print(f"\n✓ Found {len(brands)} brands:\n")
        
        for brand in brands:
            print(f"• {brand['company']}")
            print(f"  Website: {brand.get('website', 'N/A')}")
            print(f"  Email: {brand.get('email', 'N/A')}")
            print(f"  Sector: {brand.get('sector', 'N/A')}")
            print()


def demo_emails():
    """Demo email generation for existing prospects"""
    print("\n✉️  DEMO: Email Generation\n")
    
    system = ChronosOutreachSystem()
    
    # Get prospects without emails
    prospects = system.db.get_prospects_without_emails()
    
    if not prospects:
        print("No prospects found without emails.")
        print("Run the research demo first: python example.py demo-research")
        return
    
    print(f"Found {len(prospects)} prospects without email sequences.\n")
    
    response = input("Generate email sequences? (y/n): ")
    
    if response.lower() == 'y':
        for prospect in prospects[:3]:  # Limit to 3 for demo
            print(f"\nGenerating emails for: {prospect['company']}")
            
            sequence = system.email_gen.generate_sequence(prospect)
            system.db.add_email_sequence(prospect['id'], sequence)
            
            print(f"✓ Generated 3 emails")
        
        print("\n✓ Demo complete! Launch web interface to review:")
        print("  python main.py review")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'test':
            quick_test()
        elif command == 'demo-research':
            demo_research()
        elif command == 'demo-emails':
            demo_emails()
        else:
            print(f"Unknown command: {command}")
            print("Available: test, demo-research, demo-emails")
    else:
        example_workflow()
