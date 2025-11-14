#!/usr/bin/env python3
"""
Research Engine - Automated brand discovery and data enrichment
"""

import re
import logging
import requests
import anthropic
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


class BrandResearcher:
    """Finds and enriches brand data automatically"""
    
    def __init__(self, config):
        self.logger = logging.getLogger('chronos.researcher')
        self.config = config
        self.claude = anthropic.Anthropic(api_key=config['anthropic_api_key'])
        self.brave_api_key = config.get('brave_api_key')
        self.logger.info("Brand Researcher initialized")

    def _validate_email(self, email):
        """
        Validate email address format and check if it's likely to be real

        Args:
            email: Email address to validate

        Returns:
            Boolean indicating if email appears valid
        """
        if not email:
            return False

        # Basic format check
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            return False

        # Filter out common fake/invalid patterns
        invalid_patterns = [
            'noreply', 'no-reply', 'donotreply', 'do-not-reply',
            'example.com', 'test.com', 'dummy', 'fake',
            'placeholder', 'yourdomain', 'domain.com'
        ]

        email_lower = email.lower()
        if any(pattern in email_lower for pattern in invalid_patterns):
            return False

        return True

    def find_brands(self, category, limit=20):
        """
        Find brands in a specific category using web search
        
        Args:
            category: Product category (e.g., "Irish Whiskey", "Premium Gin")
            limit: Maximum number of brands to find
            
        Returns:
            List of brand dictionaries with basic info
        """
        brands = []
        
        # Search queries to find brands
        queries = [
            f"premium {category} brands list",
            f"top {category} brands 2025",
            f"luxury {category} producers",
            f"best {category} brands"
        ]
        
        for query in queries:
            if len(brands) >= limit:
                break
                
            search_results = self._web_search(query)
            
            # Use Claude to extract brand names from search results
            extracted = self._extract_brands_with_ai(search_results, category)
            
            for brand in extracted:
                if len(brands) >= limit:
                    break
                    
                # Avoid duplicates
                if not any(b['name'].lower() == brand['name'].lower() for b in brands):
                    brands.append(brand)
        
        return brands[:limit]
    
    def enrich_brand_data(self, brand):
        """
        Enrich brand data with website, contact info, and products
        
        Args:
            brand: Basic brand dictionary with at least 'name'
            
        Returns:
            Enriched brand dictionary or None if failed
        """
        enriched = brand.copy()
        
        # Step 1: Find website
        if 'website' not in enriched or not enriched['website']:
            website = self._find_website(brand['name'])
            if not website:
                return None
            enriched['website'] = website
        
        # Step 2: Scrape website for information
        website_data = self._scrape_website(enriched['website'])
        
        # Step 3: Find email address
        email = self._find_email(enriched['website'], website_data, brand['name'])
        if not email:
            return None
        enriched['email'] = email
        
        # Step 4: Extract products and company info
        company_info = self._extract_company_info(website_data, brand['name'])
        enriched.update(company_info)
        
        return enriched
    
    def _web_search(self, query):
        """
        Perform web search using Brave Search API
        """
        if not self.brave_api_key:
            # Fallback: simulate with basic search
            return self._fallback_search(query)
        
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {"q": query, "count": 10}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('web', {}).get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'description': item.get('description', '')
                })
            
            return results
        except Exception as e:
            print(f"  ⚠ Search API error: {e}")
            return self._fallback_search(query)
    
    def _fallback_search(self, query):
        """Fallback search method using DuckDuckGo HTML scraping"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result')[:10]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'description': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })
            
            return results
        except Exception as e:
            print(f"  ⚠ Fallback search error: {e}")
            return []
    
    def _extract_brands_with_ai(self, search_results, category):
        """Use Claude to extract brand names from search results"""
        if not search_results:
            return []
        
        # Format search results for Claude
        results_text = "\n\n".join([
            f"Title: {r['title']}\nURL: {r['url']}\nDescription: {r['description']}"
            for r in search_results[:10]
        ])
        
        prompt = f"""Based on these search results about {category} brands, extract a list of brand names.

Search Results:
{results_text}

Extract ONLY the actual brand/company names (not product names). Return as JSON array:
["Brand Name 1", "Brand Name 2", ...]

Return only valid JSON, nothing else."""
        
        try:
            message = self.claude.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            # Extract JSON from response
            import json
            brand_names = json.loads(response_text)
            
            return [{'name': name} for name in brand_names if name]
        
        except Exception as e:
            print(f"  ⚠ AI extraction error: {e}")
            return []
    
    def _find_website(self, brand_name):
        """Find official website for a brand"""
        search_query = f"{brand_name} official website"
        results = self._web_search(search_query)
        
        if not results:
            return None
        
        # First result is usually the official website
        url = results[0]['url']
        
        # Validate it's a real website
        if url and 'http' in url:
            return self._normalize_url(url)
        
        return None
    
    def _normalize_url(self, url):
        """Normalize URL to base domain"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _scrape_website(self, url):
        """Scrape website content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Also get all links for finding contact page
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(url, href)
                links.append({
                    'text': a.get_text(strip=True),
                    'url': full_url
                })
            
            return {
                'text': text[:10000],  # Limit text length
                'links': links,
                'html': str(soup)[:20000]
            }
        
        except Exception as e:
            print(f"  ⚠ Scraping error: {e}")
            return {'text': '', 'links': [], 'html': ''}
    
    def _find_email(self, website, website_data, brand_name):
        """Find contact email for the brand"""
        # Method 1: Look for emails in page text
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                           website_data['text'])

        if emails:
            # Filter using validation function
            valid_emails = [e for e in emails if self._validate_email(e)]
            if valid_emails:
                return valid_emails[0]
        
        # Method 2: Check contact page
        contact_links = [link for link in website_data['links'] 
                        if any(word in link['text'].lower() or word in link['url'].lower() 
                              for word in ['contact', 'about', 'press', 'media'])]
        
        for link in contact_links[:3]:  # Check first 3 contact-related pages
            try:
                contact_data = self._scrape_website(link['url'])
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                                   contact_data['text'])
                if emails:
                    valid_emails = [e for e in emails if self._validate_email(e)]
                    if valid_emails:
                        return valid_emails[0]
            except Exception as e:
                # Skip this link if scraping fails (network error, parsing error, etc.)
                print(f"  Warning: Could not scrape {link['url']}: {e}")
                continue
        
        # Method 3: Common email patterns (last resort)
        domain = urlparse(website).netloc
        if domain:
            # Clean domain (remove www. prefix if present)
            domain = domain.replace('www.', '')

            # Try common prefixes
            for prefix in ['contact', 'info', 'hello', 'press']:
                guessed_email = f"{prefix}@{domain}"
                if self._validate_email(guessed_email):
                    print(f"  ⚠ Using guessed email (please verify): {guessed_email}")
                    return guessed_email

        # If no valid email found, return None
        print(f"  ✗ Could not find valid email for {brand_name}")
        return None
    
    def _extract_company_info(self, website_data, brand_name):
        """Extract company information and products using AI"""
        prompt = f"""Analyze this website content for {brand_name} and extract:

Website Content:
{website_data['text'][:5000]}

Extract and return as JSON:
{{
    "company_name": "Official company name",
    "products": ["Product 1", "Product 2", "Product 3"],
    "description": "Brief 1-sentence company description",
    "sector": "Industry sector (e.g., Spirits, Cosmetics, Fashion)"
}}

Return only valid JSON."""
        
        try:
            message = self.claude.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            import json
            info = json.loads(response_text)
            
            return {
                'company': info.get('company_name', brand_name),
                'products': info.get('products', []),
                'description': info.get('description', ''),
                'sector': info.get('sector', 'Unknown')
            }
        
        except Exception as e:
            print(f"  ⚠ Info extraction error: {e}")
            return {
                'company': brand_name,
                'products': [],
                'description': '',
                'sector': 'Unknown'
            }
