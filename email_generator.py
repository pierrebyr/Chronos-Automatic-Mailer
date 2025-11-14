#!/usr/bin/env python3
"""
Email Sequence Generator - Creates personalized cold email sequences
"""

import logging
import anthropic
from datetime import datetime


class EmailSequenceGenerator:
    """Generates personalized email sequences for prospects"""
    
    def __init__(self, config):
        self.logger = logging.getLogger('chronos.email_generator')
        self.config = config
        self.claude = anthropic.Anthropic(api_key=config['anthropic_api_key'])
        self.logger.info("Email Sequence Generator initialized")
        
        # Load Chronos brand information
        self.chronos_info = {
            'positioning': 'Premium AI-enhanced product photography',
            'key_benefits': [
                '80% cost reduction vs traditional shoots',
                '48-72h turnaround for first drafts',
                'Studio-grade quality with AI enhancement',
                'Multi-format optimization included',
                'Full usage rights'
            ],
            'expertise': 'Over 5 years experience with luxury brands',
            'differentiator': 'Deep photography expertise + AI technology (not just automated AI)',
            'clients': ['Rémy Martin', 'Suntory Hibiki', 'Via Carota', 'Strange Nature Gin'],
            'sectors': ['Spirits', 'Cosmetics', 'Fashion', 'Luxury goods'],
            'contact': {
                'name': config.get('sender_name', 'Your Name'),
                'email': config.get('sender_email', 'your-email@example.com'),
                'phone': config.get('sender_phone', 'Your Phone'),
                'website': config.get('sender_website', 'www.chronos.studio')
            }
        }
    
    def generate_sequence(self, prospect):
        """
        Generate complete 3-email sequence for a prospect
        
        Args:
            prospect: Prospect dictionary with company, products, sector, etc.
            
        Returns:
            Dictionary with 3 emails
        """
        # Select a specific product to showcase (if available)
        showcase_product = self._select_showcase_product(prospect)
        
        # Generate each email
        email1 = self._generate_email_1(prospect, showcase_product)
        email2 = self._generate_email_2(prospect, showcase_product)
        email3 = self._generate_email_3(prospect, showcase_product)
        
        return {
            'email_1': email1,
            'email_2': email2,
            'email_3': email3
        }
    
    def _select_showcase_product(self, prospect):
        """Select the most appropriate product to showcase"""
        products = prospect.get('products', [])
        
        if not products:
            # Generic product name based on sector
            sector = prospect.get('sector', 'Product')
            return f"{prospect['company']} {sector}"
        
        # Return first product or most relevant one
        return products[0]
    
    def _generate_email_1(self, prospect, showcase_product):
        """Generate first email - introduction with demo"""
        
        prompt = f"""Create a personalized cold email for Chronos Studio (premium AI-enhanced product photography).

PROSPECT INFO:
- Company: {prospect['company']}
- Sector: {prospect.get('sector', 'Luxury goods')}
- Products: {', '.join(prospect.get('products', [])[:3])}
- Website: {prospect.get('website', '')}
- Showcase Product: {showcase_product}

CHRONOS STUDIO INFO:
- Positioning: {self.chronos_info['positioning']}
- Key Benefits: {', '.join(self.chronos_info['key_benefits'])}
- Clients: {', '.join(self.chronos_info['clients'][:3])}
- Contact: Pierre Bouyer, +33-6-72-30-92-41, www.chronos.studio

TEMPLATE STRUCTURE (adapt and personalize):
Subject: See [Product Name] Enhanced by Chronos Studio

Hi [Name],

We noticed [Company Name]'s commitment to quality in your product presentations, and we wanted to introduce you to a solution that could transform your visual content strategy while reducing costs by up to 80%.

Inspired by [specific product], we created a premium product visual (attached) to show you what's possible with our innovative approach.

At Chronos Studio, we combine premium photography expertise with advanced AI technology to deliver exceptional product visuals in 48-72 hours. Our clients in [relevant sector] are achieving stunning results without the traditional hassles of photo shoots.

What sets us apart:
- Professional-grade imagery at a fraction of traditional costs
- Lightning-fast turnaround (48-72h for first drafts)
- Unlimited variations and multi-format adaptations
- Full usage rights included

Would you be interested in seeing how we've helped similar brands transform their visual content? We'd be happy to share some relevant case studies or schedule a quick call to discuss your specific needs.

Best regards,
Pierre Bouyer
Chronos Studio

P.S. We're currently offering a special trial package for new clients - let me know if you'd like to learn more.

INSTRUCTIONS:
1. Personalize the opening by mentioning something specific about their brand/products
2. Reference their sector specifically
3. Keep professional but warm tone
4. Focus on value proposition for their specific situation
5. Make it concise (under 200 words)
6. DO NOT mention creating a demo image (we don't have it yet) - instead offer to create one

Return ONLY the email in this JSON format:
{{
    "subject": "Subject line here",
    "body": "Email body here (plain text)",
    "html_body": "Email body with HTML formatting"
}}"""

        return self._call_claude_for_email(prompt)
    
    def _generate_email_2(self, prospect, showcase_product):
        """Generate second email - follow-up emphasizing expertise"""
        
        prompt = f"""Create a follow-up email (Email #2 in sequence) for Chronos Studio.

PROSPECT INFO:
- Company: {prospect['company']}
- Sector: {prospect.get('sector', 'Luxury goods')}
- Products: {', '.join(prospect.get('products', [])[:3])}
- Showcase Product: {showcase_product}

CHRONOS STUDIO INFO:
- Differentiator: {self.chronos_info['differentiator']}
- Expertise: {self.chronos_info['expertise']}
- Clients: {', '.join(self.chronos_info['clients'])}

TEMPLATE STRUCTURE (adapt and personalize):
Subject: Re: Our Approach to Premium Product Photography + AI

Hi [Name],

I'm following up on my previous email regarding how we could elevate your product imagery while significantly reducing production costs.

What makes us truly unique in the AI-enhanced photography space is our deep-rooted expertise in premium product photography. Our team has over five years of experience working with luxury brands, and we understand that AI is just a tool - the real magic comes from our in-house expertise in professional retouching, creative direction, and premium product photography.

Unlike fully automated solutions, we combine cutting-edge technology with human craftsmanship to ensure every image meets the exacting standards of premium brands. This hybrid approach has already proven successful with clients like [mention 2-3 prestigious clients].

Would you be open to a 15-minute call this week to discuss how we could support your visual content needs?

Best regards,
Pierre Bouyer

P.S. The special trial package offer is still available for a limited time.

INSTRUCTIONS:
1. Reference the previous email naturally
2. Emphasize the expertise + AI combination (not just automation)
3. Mention relevant clients in their sector
4. Keep concise (under 150 words)
5. Clear CTA for a call

Return ONLY the email in JSON format:
{{
    "subject": "Subject line here",
    "body": "Email body here (plain text)",
    "html_body": "Email body with HTML formatting"
}}"""

        return self._call_claude_for_email(prompt)
    
    def _generate_email_3(self, prospect, showcase_product):
        """Generate third email - final touchpoint"""
        
        prompt = f"""Create a final follow-up email (Email #3 in sequence) for Chronos Studio.

PROSPECT INFO:
- Company: {prospect['company']}
- Showcase Product: {showcase_product}

TEMPLATE STRUCTURE (adapt and personalize):
Subject: Final Call: Trial Package for [Company Name]

Hi [Name],

I wanted to send you one last note about elevating {prospect['company']}'s product visuals.

As we're planning our upcoming projects, I wanted to give you a final opportunity to take advantage of our trial package offer before it expires this week.

If you're interested in transforming your product visuals while reducing costs by up to 80%, I'm still happy to schedule a quick call or share more details.

Best regards,
Pierre Bouyer
Chronos Studio
+33-6-72-30-92-41
www.chronos.studio

P.S. If timing isn't right, feel free to keep our contact information for future reference.

INSTRUCTIONS:
1. Keep it short and friendly
2. Create urgency but remain professional
3. Offer an easy out if not interested
4. Under 100 words

Return ONLY the email in JSON format:
{{
    "subject": "Subject line here",
    "body": "Email body here (plain text)",
    "html_body": "Email body with HTML formatting"
}}"""

        return self._call_claude_for_email(prompt)
    
    def _call_claude_for_email(self, prompt):
        """Call Claude API to generate email"""
        try:
            message = self.claude.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # Extract JSON from response
            import json
            
            # Remove markdown code blocks if present
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            email_data = json.loads(response_text)
            
            # Ensure we have all required fields
            if 'subject' not in email_data or 'body' not in email_data:
                raise ValueError("Missing required fields in email data")
            
            # Generate HTML version if not provided
            if 'html_body' not in email_data:
                email_data['html_body'] = self._text_to_html(email_data['body'])
            
            return email_data
        
        except Exception as e:
            print(f"  ⚠ Email generation error: {e}")
            # Return fallback template
            return self._get_fallback_email()
    
    def _text_to_html(self, text):
        """Convert plain text email to simple HTML"""
        # Replace newlines with <br>
        html = text.replace('\n\n', '</p><p>').replace('\n', '<br>')
        
        # Wrap in basic HTML structure
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <p>{html}</p>
        </body>
        </html>
        """
        
        return html
    
    def _get_fallback_email(self):
        """Return a basic fallback email if generation fails"""
        return {
            'subject': 'Transform Your Product Photography with Chronos Studio',
            'body': '''Hi,

We noticed your commitment to quality in your product presentations.

At Chronos Studio, we combine premium photography expertise with AI technology to deliver exceptional product visuals in 48-72 hours - at 80% lower cost than traditional shoots.

Would you be interested in learning how we've helped luxury brands transform their visual content?

Best regards,
Pierre Bouyer
Chronos Studio
+33-6-72-30-92-41
www.chronos.studio''',
            'html_body': '<p>Hi,</p><p>We noticed your commitment to quality in your product presentations.</p><p>At Chronos Studio, we combine premium photography expertise with AI technology to deliver exceptional product visuals in 48-72 hours - at 80% lower cost than traditional shoots.</p><p>Would you be interested in learning how we\'ve helped luxury brands transform their visual content?</p><p>Best regards,<br>Pierre Bouyer<br>Chronos Studio<br>+33-6-72-30-92-41<br>www.chronos.studio</p>'
        }
