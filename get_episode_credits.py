#!/usr/bin/env python3
"""
Script to extract director and writer information from IMDB episode pages
and update the existing CSV file with this information.
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_episode_credits(episode_url, session):
    """
    Get director and writer information from an episode page
    """
    if not episode_url:
        return None, None
        
    # Construct full URL if relative
    if episode_url.startswith('/'):
        episode_url = 'https://www.imdb.com' + episode_url
        
    try:
        logger.info(f"Fetching credits from: {episode_url}")
        response = session.get(episode_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find director and writer information
        director = None
        writer = None
        
        # Look for all name links
        all_links = soup.find_all('a')
        
        # Look for director and writer
        director_found = False
        writer_found = False
        
        for link in all_links:
            if director_found and writer_found:
                break
                
            href_attr = link.get('href')
            if href_attr and '/name/nm' in str(href_attr):
                # Check the surrounding context for director/writer indicators
                parent_element = link.parent
                if parent_element:
                    # Walk up the element tree to find context
                    current = parent_element
                    for _ in range(4):  # Check up to 4 levels up
                        if current:
                            context_text = current.get_text()
                            
                            if 'Director' in context_text and not director_found:
                                director = link.get_text(strip=True)
                                director_found = True
                                logger.info(f"Found director: {director}")
                                break
                            elif 'Writer' in context_text and not writer_found:
                                writer = link.get_text(strip=True)
                                writer_found = True
                                logger.info(f"Found writer: {writer}")
                                break
                            
                            current = current.parent if hasattr(current, 'parent') else None
        
        # Rate limit to be respectful
        time.sleep(1)
        
        return director, writer
        
    except Exception as e:
        logger.error(f"Error fetching credits from {episode_url}: {e}")
        return None, None

def get_episode_url_from_title(title, season, episode, session):
    """
    Get the episode URL by searching through the season page
    """
    season_url = f"https://www.imdb.com/title/tt0264235/episodes/?season={season}&ref_=ttep"
    
    try:
        response = session.get(season_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all episode containers
        episode_containers = soup.find_all('article', class_='episode-item-wrapper')
        
        for container in episode_containers:
            # Extract episode title and URL
            title_elem = container.find('a', class_='ipc-title-link-wrapper')
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                episode_url = title_elem.get('href')
                
                # Parse episode number from title
                match = re.search(r'S\d+\.E(\d+)\s*[∙·]\s*(.+)', title_text)
                if match:
                    ep_num = int(match.group(1))
                    ep_title = match.group(2).strip()
                    
                    if ep_num == episode and title.lower() in ep_title.lower():
                        return episode_url
                        
    except Exception as e:
        logger.error(f"Error finding episode URL for S{season}E{episode}: {e}")
        
    return None

def update_csv_with_credits():
    """
    Update the existing CSV file with director and writer information
    """
    # Setup session
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Read existing CSV
    episodes = []
    try:
        with open('curb_episodes.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            episodes = list(reader)
    except FileNotFoundError:
        logger.error("curb_episodes.csv not found. Please run the main scraper first.")
        return
    
    logger.info(f"Found {len(episodes)} episodes to update")
    
    # Update each episode with director and writer info
    for i, episode in enumerate(episodes):
        season = int(episode['season'])
        ep_num = int(episode['episode'])
        title = episode['title']
        
        logger.info(f"Processing S{season}E{ep_num}: {title} ({i+1}/{len(episodes)})")
        
        # Get episode URL
        episode_url = get_episode_url_from_title(title, season, ep_num, session)
        
        if episode_url:
            # Get credits
            director, writer = get_episode_credits(episode_url, session)
            
            # Update episode data
            episode['director'] = director or ''
            episode['writer'] = writer or ''
        else:
            logger.warning(f"Could not find URL for S{season}E{ep_num}: {title}")
            episode['director'] = ''
            episode['writer'] = ''
        
        # Progress update every 10 episodes
        if (i + 1) % 10 == 0:
            logger.info(f"Processed {i + 1}/{len(episodes)} episodes")
    
    # Write updated CSV
    fieldnames = ['season', 'episode', 'title', 'air_date', 'rating', 'votes', 'description', 'director', 'writer']
    
    with open('curb_episodes_with_credits.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer_csv = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer_csv.writeheader()
        
        for episode in episodes:
            writer_csv.writerow(episode)
    
    logger.info("Updated CSV saved as 'curb_episodes_with_credits.csv'")
    
    # Also save as JSON
    with open('curb_episodes_with_credits.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(episodes, jsonfile, indent=2, ensure_ascii=False)
    
    logger.info("Updated JSON saved as 'curb_episodes_with_credits.json'")
    
    # Print sample results
    print("\n" + "="*60)
    print("SAMPLE RESULTS WITH CREDITS")
    print("="*60)
    
    for episode in episodes[:5]:  # Show first 5 episodes
        print(f"S{episode['season']}E{episode['episode']}: {episode['title']}")
        print(f"  Director: {episode['director'] or 'Not found'}")
        print(f"  Writer: {episode['writer'] or 'Not found'}")
        print(f"  Rating: {episode['rating']}/10")
        print()

if __name__ == "__main__":
    update_csv_with_credits() 