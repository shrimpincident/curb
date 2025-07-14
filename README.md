# Curb Your Enthusiasm Episode Rating Scraper

This script scrapes episode rating information for all seasons of Curb Your Enthusiasm from IMDB.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script to scrape all 12 seasons of Curb Your Enthusiasm:

```bash
python scrape_curb_episodes.py
```

## Output

The script will create two files:
- `curb_episodes.csv` - Episode data in CSV format
- `curb_episodes.json` - Episode data in JSON format

## Data Fields

Each episode contains the following information:
- **season**: Season number (1-12)
- **episode**: Episode number within the season
- **title**: Episode title
- **air_date**: Original air date
- **rating**: IMDB rating (out of 10)
- **votes**: Number of votes for the rating
- **description**: Episode description/plot summary

## Features

- **Rate Limiting**: Includes 1-second delays between requests to be respectful to IMDB's servers
- **Error Handling**: Robust error handling for network issues and parsing errors
- **Logging**: Detailed logging of the scraping process
- **Multiple Formats**: Saves data in both CSV and JSON formats
- **Summary Statistics**: Displays summary statistics including highest/lowest rated episodes

## Example Output

```
CURB YOUR ENTHUSIASM EPISODE SCRAPING SUMMARY
============================================================
Total Episodes: 120
Total Seasons: 12

Episodes per Season:
  Season 1: 10 episodes (avg rating: 8.2)
  Season 2: 10 episodes (avg rating: 8.4)
  ...

Highest Rated Episode: S4E8 - The Car Pool Lane (9.2/10)
Lowest Rated Episode: S9E4 - Running with the Bulls (7.1/10)
```

## Notes

- The script includes proper User-Agent headers to avoid being blocked
- All data is scraped from publicly available IMDB pages
- The script is designed to be run once to collect all data
- Be respectful when scraping - the script includes rate limiting 