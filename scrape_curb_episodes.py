#!/usr/bin/env python3
"""
IMDB Curb Your Enthusiasm Episode Rating Scraper

This script scrapes episode rating information for all seasons of 
Curb Your Enthusiasm from IMDB.
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import re
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CurbEpisodeScraper:
    def __init__(self):
        self.base_url = "https://www.imdb.com/title/tt0264235/episodes/?season={}&ref_=ttep"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.episodes = []
        
    def get_season_episodes(self, season_num: int) -> List[Dict]:
        """
        Scrape episode data for a specific season
        """
        url = self.base_url.format(season_num)
        logger.info(f"Scraping season {season_num}: {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            episodes = []
            
            # Find all episode containers
            episode_containers = soup.find_all('article', class_='episode-item-wrapper')
            
            for container in episode_containers:
                episode_data = self._extract_episode_data(container, season_num)
                if episode_data:
                    episodes.append(episode_data)
                    
            logger.info(f"Found {len(episodes)} episodes in season {season_num}")
            return episodes
            
        except requests.RequestException as e:
            logger.error(f"Error fetching season {season_num}: {e}")
            return []
            
    def _extract_episode_data(self, container, season_num: int) -> Optional[Dict]:
        """
        Extract episode data from a container element
        """
        try:
            # Episode title and number
            title_elem = container.find('a', class_='ipc-title-link-wrapper')
            if not title_elem:
                return None
                
            title_text = title_elem.get_text(strip=True)
            episode_url = title_elem.get('href')
            
            # Extract episode number and title from format "S1.E1 ∙ The Pants Tent"
            episode_num = None
            title = title_text
            
            # Parse episode number from title
            match = re.search(r'S\d+\.E(\d+)\s*[∙·]\s*(.+)', title_text)
            if match:
                episode_num = int(match.group(1))
                title = match.group(2).strip()
            
            # Air date
            air_date_elem = container.find('span', class_='sc-a388aa45-10')
            air_date = air_date_elem.get_text(strip=True) if air_date_elem else None
            
            # Rating
            rating_elem = container.find('span', class_='ipc-rating-star--rating')
            rating = None
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                try:
                    rating = float(rating_text)
                except ValueError:
                    pass
            
            # Vote count
            votes_elem = container.find('span', class_='ipc-rating-star--voteCount')
            votes = None
            if votes_elem:
                votes_text = votes_elem.get_text(strip=True)
                # Remove parentheses and convert to number
                votes_text = votes_text.replace('(', '').replace(')', '').replace(',', '').replace(' ', '')
                try:
                    if 'K' in votes_text:
                        votes = int(float(votes_text.replace('K', '')) * 1000)
                    elif 'M' in votes_text:
                        votes = int(float(votes_text.replace('M', '')) * 1000000)
                    else:
                        votes = int(votes_text)
                except (ValueError, TypeError):
                    pass
            
            # Description/plot
            description_elem = container.find('div', class_='ipc-html-content-inner-div')
            description = description_elem.get_text(strip=True) if description_elem else None
            
            # Get director and writer information from episode page
            # Temporarily disabled due to complexity - will create separate script
            director, writer = None, None
            
            return {
                'season': season_num,
                'episode': episode_num,
                'title': title,
                'air_date': air_date,
                'rating': rating,
                'votes': votes,
                'description': description,
                'director': director,
                'writer': writer
            }
            
        except Exception as e:
            logger.error(f"Error extracting episode data: {e}")
            return None
    
    def _get_episode_credits(self, episode_url: str) -> tuple:
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
            response = self.session.get(episode_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find director and writer information using a simple approach
            director = None
            writer = None
            
            # Look for all name links (people)
            all_links = soup.find_all('a')
            
            # Look for spans containing "Director" or "Writer" text
            director_found = False
            writer_found = False
            
            for link in all_links:
                if director_found and writer_found:
                    break
                    
                href = link.get('href', '')
                if '/name/nm' not in href:
                    continue
                    
                # Check the surrounding context for director/writer indicators
                parent_element = link.parent
                if parent_element:
                    # Get the text of nearby elements
                    for _ in range(3):  # Check up to 3 levels up
                        if parent_element:
                            context_text = parent_element.get_text()
                            
                            if 'Director' in context_text and not director_found:
                                director = link.get_text(strip=True)
                                director_found = True
                                break
                            elif 'Writer' in context_text and not writer_found:
                                writer = link.get_text(strip=True)
                                writer_found = True
                                break
                            
                            parent_element = parent_element.parent
            
            # Rate limit to be respectful
            time.sleep(0.5)
            
            logger.info(f"Found credits - Director: {director}, Writer: {writer}")
            return director, writer
            
        except Exception as e:
            logger.error(f"Error fetching credits from {episode_url}: {e}")
            return None, None
    
    def scrape_all_seasons(self, max_seasons: int = 12) -> List[Dict]:
        """
        Scrape all seasons of Curb Your Enthusiasm
        """
        all_episodes = []
        
        for season in range(1, max_seasons + 1):
            episodes = self.get_season_episodes(season)
            all_episodes.extend(episodes)
            
            # Be respectful with rate limiting
            time.sleep(1)
            
        self.episodes = all_episodes
        return all_episodes
    
    def save_to_csv(self, filename: str = 'curb_episodes.csv'):
        """
        Save episode data to CSV file
        """
        if not self.episodes:
            logger.warning("No episodes to save")
            return
            
        fieldnames = ['season', 'episode', 'title', 'air_date', 'rating', 'votes', 'description', 'director', 'writer']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for episode in self.episodes:
                writer.writerow(episode)
                
        logger.info(f"Saved {len(self.episodes)} episodes to {filename}")
    
    def save_to_json(self, filename: str = 'curb_episodes.json'):
        """
        Save episode data to JSON file
        """
        if not self.episodes:
            logger.warning("No episodes to save")
            return
            
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.episodes, jsonfile, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved {len(self.episodes)} episodes to {filename}")
    
    def print_summary(self):
        """
        Print a summary of scraped data
        """
        if not self.episodes:
            logger.warning("No episodes scraped")
            return
            
        seasons = {}
        total_episodes = len(self.episodes)
        
        for episode in self.episodes:
            season = episode['season']
            if season not in seasons:
                seasons[season] = []
            seasons[season].append(episode)
        
        print("\n" + "="*60)
        print("CURB YOUR ENTHUSIASM EPISODE SCRAPING SUMMARY")
        print("="*60)
        print(f"Total Episodes: {total_episodes}")
        print(f"Total Seasons: {len(seasons)}")
        print("\nEpisodes per Season:")
        
        for season in sorted(seasons.keys()):
            episode_count = len(seasons[season])
            avg_rating = sum(ep['rating'] for ep in seasons[season] if ep['rating']) / len([ep for ep in seasons[season] if ep['rating']])
            print(f"  Season {season}: {episode_count} episodes (avg rating: {avg_rating:.1f})")
        
        # Find highest and lowest rated episodes
        rated_episodes = [ep for ep in self.episodes if ep['rating']]
        if rated_episodes:
            highest_rated = max(rated_episodes, key=lambda x: x['rating'])
            lowest_rated = min(rated_episodes, key=lambda x: x['rating'])
            
            print(f"\nHighest Rated Episode: S{highest_rated['season']}E{highest_rated['episode']} - {highest_rated['title']} ({highest_rated['rating']}/10)")
            print(f"Lowest Rated Episode: S{lowest_rated['season']}E{lowest_rated['episode']} - {lowest_rated['title']} ({lowest_rated['rating']}/10)")


def main():
    """
    Main function to run the scraper
    """
    scraper = CurbEpisodeScraper()
    
    print("Starting Curb Your Enthusiasm episode scraping...")
    print("This may take a few minutes to complete...")
    
    # Scrape all seasons
    episodes = scraper.scrape_all_seasons(12)
    
    if episodes:
        # Save data in multiple formats
        scraper.save_to_csv()
        scraper.save_to_json()
        
        # Print summary
        scraper.print_summary()
        
        print(f"\nScraping complete! Found {len(episodes)} episodes.")
        print("Data saved to:")
        print("  - curb_episodes.csv")
        print("  - curb_episodes.json")
    else:
        print("No episodes were scraped. Please check the logs for errors.")


if __name__ == "__main__":
    main() 