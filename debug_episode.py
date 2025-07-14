#!/usr/bin/env python3
"""
Debug script to examine the HTML structure of an individual episode page
"""

import requests
from bs4 import BeautifulSoup

def debug_episode_page():
    # Test with the first episode
    url = "https://www.imdb.com/title/tt0551416/?ref_=ttep_ep_1"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        response = session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save the HTML to a file for inspection
        with open('episode_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print("Episode page saved to episode_page.html")
        print(f"Status code: {response.status_code}")
        print(f"Page length: {len(response.text)} characters")
        
        # Look for various credit selectors
        print("\n--- Searching for director/writer information ---")
        
        # Try different selectors for credits
        selectors = [
            'section[data-testid="title-crew"]',
            'li[data-testid*="crew-item"]',
            'div.credit_summary_item',
            'ul.cast_list',
            'div.titlePageSprite',
            'span.ghost',
            'div.txt-block'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                for i, elem in enumerate(elements[:2]):  # Show first 2
                    print(f"  {i+1}: {elem.get_text()[:200]}...")
                    
        # Look for text containing "Director" or "Writer"
        print("\n--- Searching for Director/Writer text ---")
        director_text = soup.find_all(string=lambda text: text and 'Director' in text)
        writer_text = soup.find_all(string=lambda text: text and 'Writer' in text)
        
        print(f"Found {len(director_text)} elements containing 'Director'")
        for text in director_text[:3]:
            parent = text.parent if text.parent else None
            if parent:
                print(f"  Director text: '{text}' in {parent.name} with classes {parent.get('class', [])}")
                
        print(f"Found {len(writer_text)} elements containing 'Writer'")
        for text in writer_text[:3]:
            parent = text.parent if text.parent else None
            if parent:
                print(f"  Writer text: '{text}' in {parent.name} with classes {parent.get('class', [])}")
                
        # Look for name links (pattern: /name/nm...)
        print("\n--- Searching for name links ---")
        name_links = soup.find_all('a', href=lambda href: href and '/name/nm' in href)
        print(f"Found {len(name_links)} name links")
        for i, link in enumerate(name_links[:5]):
            print(f"  {i+1}: {link.get_text()} -> {link.get('href')}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_episode_page() 